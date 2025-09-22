import streamlit as st
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import os

# --- Configuration ---
CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "gemini-1.5-flash"

# --- Initialize session state ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

def load_components(api_key):
    """Load ChromaDB and create QA chain"""
    try:
        os.environ["GOOGLE_API_KEY"] = api_key
        embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
        llm = ChatGoogleGenerativeAI(
            model=LLM_MODEL_NAME, 
            temperature=0.2, 
            convert_system_message_to_human=True
        )
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True
        )
        return qa_chain
    except Exception as e:
        st.error(f"Failed to load components: {e}")
        return None

def format_timestamp_link(video_url, start_time):
    """Format video URL with timestamp"""
    return f"{video_url}&t={int(start_time)}s"

def main():
    # Page configuration
    st.set_page_config(
        page_title="Fireship Chat",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Title and description
    st.title("🔥 Chat with Fireship's YouTube Channel")
    st.markdown("Ask questions about Fireship's '100 Seconds of Code' videos and get answers powered by Google Gemini!")
    
    # Sidebar for API key configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        if not st.session_state.api_key_configured:
            st.markdown("**Step 1:** Enter your Google AI API Key")
            google_api_key = st.text_input(
                "Google AI API Key:", 
                type="password",
                help="Get your API key from https://makersuite.google.com/app/apikey"
            )
            
            if st.button("Configure API Key", type="primary"):
                if google_api_key:
                    with st.spinner("Loading components..."):
                        qa_chain = load_components(google_api_key)
                        if qa_chain:
                            st.session_state.qa_chain = qa_chain
                            st.session_state.api_key_configured = True
                            st.success("✅ API key configured successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to configure API key. Please check your key and try again.")
                else:
                    st.error("Please enter a valid API key.")
        else:
            st.success("✅ API Key Configured")
            st.markdown("**Step 2:** You can now close this sidebar and start chatting!")
            
            if st.button("Reset API Key"):
                st.session_state.api_key_configured = False
                st.session_state.qa_chain = None
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This app searches through Fireship's YouTube transcripts to answer your questions about programming concepts, tools, and technologies.")
        
        if st.session_state.messages:
            if st.button("Clear Chat History"):
                st.session_state.messages = []
                st.rerun()
    
    # Main chat interface
    if not st.session_state.api_key_configured:
        st.info("👈 Please configure your Google AI API Key in the sidebar to get started.")
        return
    
    # Chat interface
    st.markdown("### 💬 Chat")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("🔗 View Sources"):
                    for source in message["sources"]:
                        st.markdown(f"**🎥 Video Moment:** [{source['link']}]({source['link']})")
                        st.markdown(f"> {source['content'][:200]}...")
                        st.markdown("---")
    
    # Chat input
    if prompt := st.chat_input("Ask about any programming topic covered in Fireship videos..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching through Fireship videos..."):
                try:
                    response = st.session_state.qa_chain({"query": prompt})
                    answer = response["result"]
                    
                    # Display answer
                    st.write(answer)
                    
                    # Prepare sources
                    sources = []
                    for doc in response["source_documents"]:
                        video_url = doc.metadata['video_url']
                        start_time = doc.metadata['start_time']
                        timestamp_link = format_timestamp_link(video_url, start_time)
                        
                        sources.append({
                            "link": timestamp_link,
                            "content": doc.page_content
                        })
                    
                    # Display sources in expandable section
                    if sources:
                        with st.expander("🔗 View Sources"):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**🎥 Source {i}:** [{source['link']}]({source['link']})")
                                st.markdown(f"> {source['content'][:200]}...")
                                if i < len(sources):
                                    st.markdown("---")
                    
                    # Add assistant message to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })

if __name__ == "__main__":
    main()