# TranscriptoLearn

**TranscriptoLearn** is an intelligent learning assistant that transforms **YouTube educational videos** into structured **study materials** and **interactive Q&A experiences** using modern AI techniques. It leverages **Groq's LLaMA 3**, **FAISS**, and **SentenceTransformers** for fast, contextual learning.

---

## Features

- 🎬 **Smart Transcript Extraction** - Robust YouTube transcript retrieval with multi-language support
- 🧠 **AI-Generated Study Materials** - Structured notes and summaries using LLaMA 3
- 💬 **Interactive Q&A Chat** - Ask questions about video content with semantic search
- 📱 **Responsive Web Interface** - Clean, modern UI built with React and Tailwind CSS
- 🔍 **Vector Search** - FAISS-powered semantic search for accurate content retrieval
- ⚡ **Fast Processing** - Groq API for lightning-fast AI responses

## Tech Stack

- **Flask** - Python web framework for API
- **React 18** - Modern frontend with hooks
- **Groq API** - LLaMA 3-8b-8192 model access
- **FAISS** - Vector database for semantic search
- **SentenceTransformers** - Text embeddings (all-MiniLM-L6-v2)
- **YouTube Transcript API** - Transcript extraction

## Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/your-username/TranscriptoLearn.git
cd TranscriptoLearn
```

2. **Install dependencies**
```bash
# Backend setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd client && npm install && cd ..
```

3. **Set up environment**
```bash
# Create .env file and add your Groq API key
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

4. **Run the application**
```bash
# Start backend (Terminal 1)
python app.py

# Start frontend (Terminal 2)
cd client && npm start
```
Visit `http://localhost:3000` to access the application.

## Usage

1. **Process Video** - Paste any YouTube lecture URL into the interface
2. **AI Processing** - Wait 30-60 seconds for transcript extraction and AI analysis  
3. **Study Materials** - Access generated notes, summaries, and full transcripts
4. **Interactive Learning** - Ask questions via the Q&A chatbot with semantic search
5. **Export Content** - Download materials for offline study

### Example URLs for Testing
```
- https://youtu.be/dcXqhMqhZUo?si=pZRpmWLvf5O6vr4v
- https://youtu.be/pzo13OPXZS4?si=H3PW2wIZJk8RwG5Q
- https://youtu.be/4-ylnyARFHE?si=Db7ZOS03eJ20NwO-
- https://youtu.be/MdeQMVBuGgY?si=wrLx-G5NbXdbsVXM
- https://youtu.be/XmgmUt1iFtE?si=QrAbi5HmlC7GUKLo
```

## Requirements

- Python 3.8+
- Node.js 16+
- Groq API key (free at [groq.com](https://groq.com))

## Conclusion

TranscriptoLearn bridges the gap between passive video consumption and active learning by leveraging cutting-edge AI technology. Transform lengthy lecture videos into structured notes and enable interactive Q&A sessions to maximize learning efficiency for students and educators alike.