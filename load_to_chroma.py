import pandas as pd
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import shutil

# --- Configuration ---
PLAYLIST_URL = "https://www.youtube.com/playlist?list=PL0vfts4VzfNiI1BsIK5u7LpPaIDKMJIDN"
MAX_VIDEOS_TO_PROCESS = 20
CHROMA_DB_PATH = "./chroma_db"
CHUNK_SIZE = 1000  # Target size for each text chunk in characters
CHUNK_OVERLAP = 200  # Overlap between chunks to maintain context

# --- Part 1: Data Fetching (Integrated from fireship_data.py) ---

def get_video_urls(playlist_url, max_videos=None):
    print(f"Fetching video URLs from playlist using yt-dlp: {playlist_url}")
    ydl_opts = {'quiet': True, 'extract_flat': True, 'force_generic_extractor': True}
    video_urls = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_dict = ydl.extract_info(playlist_url, download=False)
            for video in playlist_dict.get('entries', []):
                if video and 'url' in video:
                    video_urls.append(video['url'])
    except Exception as e:
        print(f"An error occurred with yt-dlp: {e}")
        return []
        
    if max_videos:
        video_urls = video_urls[:max_videos]
    print(f"Finished fetching {len(video_urls)} video URLs.")
    return video_urls

# --- Part 2: Smart Chunking with Timestamps ---

def create_chunks_with_timestamps(video_url, chunk_size, chunk_overlap):
    """
    Fetches transcript and splits it into chunks with timestamps using proper text splitting.
    """
    try:
        video_id = video_url.split("=")[-1]
        print(f"  Attempting to fetch transcript for video ID: {video_id}")
        
        # Initialize the YouTubeTranscriptApi instance
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch transcript using the new API method
        fetched_transcript = ytt_api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
        
        # Combine all transcript text with timestamps
        full_transcript = ""
        timestamp_map = {}  # Maps character positions to timestamps
        current_pos = 0
        
        for snippet in fetched_transcript:
            text_to_add = snippet.text + " "
            timestamp_map[current_pos] = snippet.start
            full_transcript += text_to_add
            current_pos += len(text_to_add)
        
        # Use RecursiveCharacterTextSplitter for better chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        )
        
        # Split the text into chunks
        text_chunks = text_splitter.split_text(full_transcript)
        
        # Find the timestamp for each chunk
        chunks = []
        search_start = 0
        
        for chunk_text in text_chunks:
            # Find where this chunk starts in the original text
            chunk_start_pos = full_transcript.find(chunk_text, search_start)
            if chunk_start_pos == -1:
                # Fallback: use the last known position
                chunk_start_pos = search_start
            
            # Find the closest timestamp
            closest_timestamp = 0
            for pos, timestamp in timestamp_map.items():
                if pos <= chunk_start_pos:
                    closest_timestamp = timestamp
                else:
                    break
            
            chunks.append({
                "text": chunk_text.strip(),
                "start_time": closest_timestamp
            })
            
            # Update search start for next chunk
            search_start = chunk_start_pos + len(chunk_text)
        
        print(f"  Successfully created {len(chunks)} chunks for video {video_id}")
        return chunks

    except (NoTranscriptFound, TranscriptsDisabled):
        print(f"  No transcript available for {video_url}. Skipping.")
        return []
    except Exception as e:
        print(f"  An error occurred with video {video_url}: {e}")
        return []

# --- Part 3: Create Embeddings and Load into ChromaDB ---

def create_and_load_embeddings(docs, chroma_db_path):
    print("\nCreating embeddings and loading into ChromaDB...")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Create ChromaDB instance from documents
    vectordb = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=chroma_db_path
    )
    
    print(f"Successfully loaded {len(docs)} chunks into ChromaDB at {chroma_db_path}.")
    return vectordb

# --- Main Execution ---
if __name__ == "__main__":
    # Clean up old database if it exists
    if os.path.exists(CHROMA_DB_PATH):
        print(f"Removing old database at {CHROMA_DB_PATH}")
        shutil.rmtree(CHROMA_DB_PATH)

    # 1. Get video URLs
    video_urls = get_video_urls(PLAYLIST_URL, MAX_VIDEOS_TO_PROCESS)
    
    all_docs = []
    if video_urls:
        # 2. Process each video
        for video_url in video_urls:
            print(f"Processing video: {video_url}")
            # Get chunks with text and start times
            chunks = create_chunks_with_timestamps(video_url, CHUNK_SIZE, CHUNK_OVERLAP)
            
            # Create LangChain Document objects with metadata
            for chunk in chunks:
                new_doc = Document(
                    page_content=chunk['text'],
                    metadata={
                        "video_url": video_url,
                        "start_time": chunk['start_time'] # IMPORTANT: We are saving the start time here
                    }
                )
                all_docs.append(new_doc)
    
    # 3. Create and load embeddings
    if all_docs:
        vector_database = create_and_load_embeddings(all_docs, CHROMA_DB_PATH)
        print("\nChromaDB setup complete with timestamps. Ready for querying!")
    else:
        print("\nNo documents were created. Database not built.")