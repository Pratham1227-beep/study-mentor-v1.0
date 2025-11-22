# 📚 AI Study Mentor - RAG-Powered Chatbot

A beautiful, intelligent study companion chatbot with RAG (Retrieval-Augmented Generation) capabilities that helps students study more effectively by analyzing their uploaded notes and PDFs.

## ✨ Features

### 🧠 **RAG-Powered Intelligence**
- **Upload PDF files and text documents**
- **AI analyzes your study materials**
- **Get personalized answers based on your notes**
- **Context-aware responses for better learning**
- **Pinned Files**: Uploaded files are displayed at the top for easy reference

### 💬 **Smart Features**
- **Conversational chat interface**
- **WhatsApp-style Chat Interface** (Green/White bubbles)
- **Message timestamps**

### ⚡ **Powered By**
- **Groq API** - Ultra-fast AI inference
- **Llama 3.3 70B** - Advanced language model
- **Streamlit** - Beautiful web interface
- **PyPDF2** - PDF text extraction

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Groq API key (free at https://console.groq.com/keys)

### Installation

1. **Clone or download this project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your API key**
   - Create a `.env` file in the project directory
   - Add your Groq API key:
   ```
   GROQ_API_KEY="your-complete-api-key-here"
   ```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

## 📖 How to Use

### Upload Study Materials
1. Click the **➕ button** on the left of the input bar
2. Select your PDF or TXT files
3. Click "Upload" to process them
4. Your files will appear pinned at the top of the chat

### Chat with AI
1. Type your question in the **fixed input bar** at the bottom
2. Press **Enter** to send
3. Get instant, context-aware responses based on your uploaded notes

### Example Questions
- "Summarize my notes on Chapter 3"
- "Create 5 quiz questions from my materials"
- "Explain the key concepts in simple terms"
- "What are the most important points to remember?"
- "Help me prepare for my exam on this topic"

## 🎯 Use Cases

- **Exam Preparation** - Get quiz questions and summaries
- **Concept Clarification** - Ask questions about your notes
- **Study Planning** - Get advice on how to study effectively
- **Quick Reviews** - Summarize long documents
- **Practice Tests** - Generate questions from your materials

## 🛠️ Technical Details

### File Support
- **PDF files** - Automatically extracts text from all pages
- **Text files** - Supports .txt format
- **Multiple files** - Upload multiple documents at once

### RAG Implementation
- Extracts text from uploaded documents
- Includes content in AI context (up to 3000 chars per document)
- AI references specific parts of your materials

## 📊 Project Structure

```
Student Mentor/
├── app.py              # Main application
├── .env                # API keys (not in git)
├── requirements.txt    # Python dependencies
├── TROUBLESHOOTING.md # Detailed help guide
└── README.md          # This file
```

## 🔒 Privacy & Security

- All processing happens in real-time
- No data is permanently stored
- Files are only kept in session memory
- Clear materials anytime with one click

## 🐛 Troubleshooting

### "Model Output Error" or API Issues
1. Run the diagnostic script:
   ```bash
   python test_api.py
   ```
2. Check `TROUBLESHOOTING.md` for detailed steps
3. Ensure your API key in `.env` is complete (starts with `gsk_` and is 100+ chars)

### PDF not processing
- Ensure the PDF is not password-protected
- Try with a different PDF file
- Check that PyPDF2 is installed

### App not loading
- Restart the Streamlit server
- Clear browser cache
- Check console for errors

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Credits

- Built with Streamlit
- Powered by Groq API
- Uses Llama 3.3 70B model
- PDF processing with PyPDF2

---

**Made with ❤️ for students who want to study smarter, not harder!**

