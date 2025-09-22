# 🔥 Fireship YouTube Chat Bot

An intelligent chat interface that allows you to ask questions about programming concepts, tools, and technologies covered in Fireship's "100 Seconds of Code" YouTube videos. Get instant answers with direct links to specific video moments!

**[▶️ Watch the Demo Video](https://drive.google.com/file/d/1mNGUhda4ULq9IS06RjKabm0JfCDIjOqx/view?usp=sharing)**

## ✨ Features

### 🎯 **Smart Video Search**
- Search through transcripts of Fireship's YouTube videos
- Get precise answers to programming questions
- Direct links to exact video timestamps where topics are discussed

### 💬 **Interactive Chat Interface**
- Clean, ChatGPT-style conversation interface
- Persistent chat history during your session
- Real-time responses powered by Google Gemini AI

### 🔗 **Source Attribution**
- Every answer includes clickable YouTube links
- Jump directly to the video moment where the topic is explained
- Preview content snippets for context

### ⚙️ **Easy Configuration**
- Simple one-time API key setup
- Collapsible sidebar for distraction-free chatting
- Clear setup instructions and status indicators

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11 or higher
- Google AI API key (free from Google AI Studio)

### Step 1: Clone & Install Dependencies
1. Download or clone the project files
2. Install required Python packages:
   - streamlit
   - langchain
   - langchain-google-genai
   - youtube-transcript-api
   - yt-dlp
   - sentence-transformers
   - chromadb
   - pandas

### Step 2: Build the Knowledge Base
1. Run the ChromaDB setup script first to download and process video transcripts
2. This creates a local vector database with embedded video content
3. The process may take 10-15 minutes depending on your internet connection

### Step 3: Get Your API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free account if you don't have one
3. Generate a new API key
4. Keep this key secure - you'll need it to run the chat interface

### Step 4: Launch the App
1. Start the Streamlit application
2. Enter your Google AI API key in the sidebar
3. Wait for the "API Key Configured" success message
4. Close the sidebar and start chatting!

## 🚀 How to Use

### Getting Started
1. **Configure API**: Enter your Google AI API key in the sidebar
2. **Start Chatting**: Type your programming questions in the chat input
3. **Explore Sources**: Click "View Sources" to see relevant video clips
4. **Navigate Videos**: Click timestamp links to jump to exact moments

### Example Questions You Can Ask
- "What is Docker and how does it work?"
- "Explain the difference between React and Vue"
- "How do I use Git for version control?"
- "What are the benefits of TypeScript?"
- "Tell me about microservices architecture"
- "How does machine learning work?"

### Tips for Better Results
- **Be Specific**: Ask about particular technologies or concepts
- **Use Context**: Reference specific tools, frameworks, or programming languages
- **Follow Up**: Ask clarifying questions based on the responses
- **Check Sources**: Click on the video links to see the full explanation

## 📊 What's Inside

### Video Content Coverage
- **Programming Languages**: JavaScript, Python, TypeScript, Rust, Go, and more
- **Web Development**: React, Vue, Angular, Node.js, Next.js
- **Cloud & DevOps**: Docker, Kubernetes, AWS, Firebase, Vercel
- **Databases**: MongoDB, PostgreSQL, Redis, Supabase
- **Tools & Frameworks**: Git, VS Code, Tailwind CSS, and many others

### Technical Architecture
- **Vector Database**: ChromaDB for semantic search
- **Embeddings**: Sentence transformers for text similarity
- **LLM**: Google Gemini 1.5 Flash for response generation
- **UI Framework**: Streamlit for the web interface
- **Data Source**: YouTube transcript API for video content

## 🔧 Troubleshooting

### Common Issues

**"API Key Configuration Failed"**
- Verify your Google AI API key is correct
- Check your internet connection
- Ensure you have API quota remaining

**"ChromaDB Not Found"**
- Run the database setup script first
- Check that the `chroma_db` folder exists in your project directory
- Verify the database was built successfully

**"No Transcript Available"**
- Some videos may not have transcripts
- The system automatically skips videos without available transcripts
- Try asking about more common programming topics

**Slow Response Times**
- First-time queries may be slower as the system loads
- Subsequent queries should be faster
- Check your internet connection for API calls

### Performance Tips
- **Restart Session**: If responses become slow, restart the Streamlit app
- **Clear Chat**: Use the "Clear Chat History" button to reset
- **Specific Questions**: More specific questions yield better, faster results

## 🤝 Contributing

### Expanding the Knowledge Base
- Add more YouTube playlists to the configuration
- Increase the `MAX_VIDEOS_TO_PROCESS` limit
- Include additional programming channels (requires modification)

### Improving Accuracy
- Adjust chunk sizes for better context preservation
- Experiment with different embedding models
- Fine-tune the retrieval parameters

## 📄 License

This project is for educational and personal use. Please respect YouTube's terms of service and the original content creators' rights.

## 🙏 Acknowledgments

- **Fireship** for creating amazing programming content
- **Google** for providing the Gemini AI API
- **LangChain** for the RAG framework
- **Streamlit** for the web interface framework

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Verify your API key and database setup
3. Ensure all dependencies are installed correctly
4. Try restarting the application

---

**Happy Learning! 🔥** Start exploring programming concepts with the power of AI and direct video references!
