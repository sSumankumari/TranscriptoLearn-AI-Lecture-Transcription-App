import os
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from sentence_transformers import SentenceTransformer
from services.faiss_service import FAISSService

CHUNK_SIZE = 500      # Number of words per chunk
CHUNK_OVERLAP = 100   # Overlap between chunks for context
EMBEDDINGS_DIR = "embeddings"

class TranscriptService:
    def __init__(self):
        # Use a small, fast, and accurate model for semantic search
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.faiss_service = FAISSService(dim=self.model.get_sentence_embedding_dimension())
        os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

    def get_transcript(self, video_id):
        """
        Fetch the transcript from YouTube using youtube_transcript_api.
        Returns the full transcript string and the raw list.
        """
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([entry['text'] for entry in transcript_list])
        return transcript, transcript_list

    def chunk_transcript(self, text):
        """
        Chunk the transcript into overlapping word windows for embeddings.
        """
        words = text.split()
        chunks = []
        for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
            chunk = ' '.join(words[i:i+CHUNK_SIZE])
            if chunk:
                chunks.append(chunk)
        return chunks

    def embed_and_store(self, video_id, chunks):
        """
        Compute embeddings for transcript chunks and store them with FAISS.
        """
        vectors = self.model.encode(chunks, show_progress_bar=False)
        self.faiss_service.add_video_embeddings(video_id, vectors, chunks)

    def semantic_search(self, video_id, question, top_k=3):
        """
        Embed a user question and retrieve the most relevant transcript chunks using FAISS.
        """
        question_vec = self.model.encode([question])
        return self.faiss_service.semantic_search(video_id, question_vec, top_k)

    def get_video_info(self, video_id):
        """
        Retrieve YouTube video metadata using yt-dlp.
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                return {
                    'title': info.get('title', 'Unknown Title'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown')
                }
        except Exception:
            return {'title': 'Unknown Title', 'duration': 0, 'uploader': 'Unknown'}