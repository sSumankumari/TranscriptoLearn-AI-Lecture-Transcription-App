# TranscriptoLearn

AI-powered lecture video transcription and learning assistant using GroqAPI and LLaMA 3.

## Features

- Extract transcripts from YouTube lecture videos
- Generate AI-powered smart notes and summaries
- Interactive Q&A chatbot for video content
- Clean, structured note formatting

## Tech Stack

- **Backend:** Flask, Groq API (LLaMA 3)
- **Frontend:** React.js
- **APIs:** YouTube Transcript API, yt-dlp
- **AI:** LangChain, FAISS embeddings

## Quick Start

1. **Clone and setup**
```bash
git clone https://github.com/your-username/TranscriptoLearn.git
cd TranscriptoLearn
python -m venv venv
# Mac/Linux: source venv/bin/activate  
venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment setup**
```bash
# Create .env file
GROQ_API_KEY=your_groq_api_key_here
```

3. **Run the application**
```bash
# Backend
python app.py

# Frontend (in new terminal)
cd client
npm install
npm start
```

Visit `http://localhost:3000`

## Example YTvideo URLs
- https://youtu.be/dcXqhMqhZUo?si=pZRpmWLvf5O6vr4v
- https://youtu.be/pzo13OPXZS4?si=H3PW2wIZJk8RwG5Q

## Usage

1. Paste a YouTube lecture video URL
2. Get AI-generated notes and summary
3. Ask questions about the content via chatbot
4. Export notes for studying

## Conclusion

TranscriptoLearn bridges the gap between passive video consumption and active learning by leveraging cutting-edge AI technology. By transforming lengthy lecture videos into structured notes and enabling interactive Q&A sessions, this tool empowers students and educators to maximize their learning efficiency. The integration of GroqAPI with LLaMA 3 ensures high-quality content processing, making complex educational material more accessible and engaging for learners of all levels.
