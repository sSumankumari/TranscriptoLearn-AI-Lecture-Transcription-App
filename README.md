# 🎓 TranscriptoLearn – AI-Powered Lecture Learning Assistant

**TranscriptoLearn** transforms YouTube educational videos into structured study materials and enables interactive Q&A using **Retrieval-Augmented Generation (RAG)** with **Groq's LLaMA 3**, **FAISS**, and **SentenceTransformers**.

---

## 🚀 Features

* 🎬 **Smart Transcript Extraction** – Robust YouTube transcript retrieval with multi-language support
* 🧠 **AI-Generated Study Materials** – Structured notes and summaries using LLaMA 3
* 💬 **Interactive Q&A Chatbot** – Ask contextual questions with semantic search
* 🔍 **Semantic Vector Search** – FAISS-powered embeddings for accurate retrieval
* ⚡ **High-Speed Inference** – Groq API for ultra-fast LLM responses
* 📱 **Modern Responsive UI** – Clean React 18 + Tailwind CSS interface

---

## 🧠 How It Works

1. User submits a YouTube lecture URL
2. Transcript extracted via YouTube Transcript API
3. Transcript chunked into meaningful sections
4. Chunks converted to embeddings (SentenceTransformers)
5. Embeddings stored in FAISS vector database
6. On query:
   * Relevant chunks retrieved via semantic search
   * Groq LLaMA 3 generates context-aware answers
7. React frontend displays notes, summaries, and Q&A responses

> **RAG Pipeline:** Retrieval + LLM Generation = Accurate, context-grounded answers

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Flask, Python 3.8+ |
| **AI/ML** | Groq API (LLaMA 3.1-8b), SentenceTransformers, FAISS |
| **Frontend** | React 18, Tailwind CSS, Axios |
| **Video Processing** | YouTube Transcript API, yt-dlp |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8+ (backend & AI pipeline)
- Node.js 16+ (for React frontend development)
- Groq API key (free at [groq.com](https://groq.com))

### Installation

```bash
# Clone repository
git clone https://github.com/sSumankumari/TranscriptoLearn-AI-Lecture-Transcription-App
cd TranscriptoLearn

# Backend setup
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

# Frontend setup
cd client && npm install && cd ..

# Environment setup
echo "GROQ_API_KEY=your_groq_api_key_here" > .env
```

### Run Application

```bash
# Terminal 1 – Backend
python app.py

# Terminal 2 – Frontend
cd client && npm start
```

Visit **http://localhost:3000**

---

## 📖 Usage

1. Paste YouTube lecture URL
2. Wait for transcript extraction & AI processing (20–90 seconds)
3. Access:
   * 📝 Structured study notes
   * 📋 AI-generated summaries
   * 📄 Full transcript
4. Ask questions using Q&A chatbot
5. Download or copy materials

### Test Videos
```
https://youtu.be/dcXqhMqhZUo
https://youtu.be/pzo13OPXZS4
https://youtu.be/4-ylnyARFHE
https://youtu.be/MdeQMVBuGgY
https://youtu.be/XmgmUt1iFtE
```

---

## 📦 Project Structure

```
TranscriptoLearn/
├── routes/
│   └── api.py              # REST API endpoints
├── services/
│   ├── transcript_service.py  # Transcript extraction & chunking
│   ├── groq_service.py       # LLM orchestration
│   └── faiss_service.py      # Vector database operations
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   └── App.js         # Main app
│   └── package.json
├── utils/
│   └── helpers.py         # Utility functions
├── app.py                 # Flask main app
└── requirements.txt       # Python dependencies
```

---

## 🎯 Key Technical Highlights

✅ **RAG Pipeline Implementation** – Semantic search + LLM generation  
✅ **Vector Database** – FAISS indexing for fast retrieval  
✅ **Error Handling** – Graceful fallbacks for unavailable transcripts  
✅ **Production-Ready** – CORS, environment variables, modular services  
✅ **Responsive UI** – React hooks, smooth animations, mobile-friendly  

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/process-video` | Process YouTube video → generate notes & summary |
| POST | `/api/ask-question` | Ask question → retrieve answer from transcript |
| GET | `/api/health` | Health check |

---

## ⚖️ License & Disclaimer

Open source for educational and commercial use.  
Transcript availability depends on YouTube and content creator permissions.

---

## 🔗 Links

* **GitHub:** [Repository](https://github.com/sSumankumari/TranscriptoLearn-AI-Lecture-Transcription-App)
* **Groq API:** [https://groq.com](https://groq.com)
* **FAISS:** [Facebook AI Similarity Search](https://faiss.ai/)