import os
import yt_dlp
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript
)
from sentence_transformers import SentenceTransformer
from services.faiss_service import FAISSService

CHUNK_SIZE = 500      # Number of words per chunk
CHUNK_OVERLAP = 100   # Overlap between chunks for context
EMBEDDINGS_DIR = "embeddings"

class TranscriptService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.faiss_service = FAISSService(dim=self.model.get_sentence_embedding_dimension())
        os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

    def get_transcript(self, video_id):
        """
        Robustly fetches a transcript for a YouTube video.
        - Tries English/manual, English/auto, any/manual, any/auto.
        - Handles both dict and object snippet types.
        - Handles all known errors and returns available languages if not found.
        Returns: transcript_text, transcript_data, transcript_language (always a string)
        """

        def to_text_list(transcript_data):
            # Handles both dict and object entries
            result = []
            for entry in transcript_data:
                if hasattr(entry, 'text'):
                    result.append(entry.text)
                elif isinstance(entry, dict) and 'text' in entry:
                    result.append(entry['text'])
                else:
                    result.append(str(entry))
            return result

        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            transcript_data = None
            lang_used = "unknown"

            # Try: manually created English
            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
                transcript_data = list(transcript.fetch())
                lang_used = getattr(transcript, "language_code", "unknown")
            except Exception:
                transcript_data = None

            # Try: auto-generated English
            if not transcript_data:
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                    transcript_data = list(transcript.fetch())
                    lang_used = getattr(transcript, "language_code", "unknown")
                except Exception:
                    transcript_data = None

            # Try: manually created any language
            if not transcript_data:
                for t in list(transcript_list._manually_created_transcripts):
                    try:
                        transcript_data = list(t.fetch())
                        lang_used = getattr(t, "language_code", "unknown")
                        break
                    except Exception:
                        continue

            # Try: auto-generated any language
            if not transcript_data:
                for t in list(transcript_list._generated_transcripts):
                    try:
                        transcript_data = list(t.fetch())
                        lang_used = getattr(t, "language_code", "unknown")
                        break
                    except Exception:
                        continue

            # If found, return transcript
            if transcript_data and len(transcript_data) > 0:
                transcript_text = ' '.join(to_text_list(transcript_data))
                return transcript_text, transcript_data, lang_used

            # If not found, return available languages for diagnostics
            available_languages = []
            for t in list(transcript_list._manually_created_transcripts) + list(transcript_list._generated_transcripts):
                try:
                    available_languages.append(
                        f"{getattr(t, 'language_code', 'unknown')} ({getattr(t, 'language', 'unknown')})")
                except Exception:
                    available_languages.append(str(getattr(t, 'language_code', 'unknown')))
            raise ValueError(
                "No transcript available for this video in any language. "
                f"Available languages for this video: {', '.join(available_languages)}"
            )

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, CouldNotRetrieveTranscript) as e:
            raise ValueError("No transcript available for this video. Please try another video URL.") from e
        except Exception as e:
            raise ValueError(f"Could not retrieve a transcript for this video: {str(e)}") from e

    def chunk_transcript(self, text):
        words = text.split()
        chunks = []
        for i in range(0, len(words), CHUNK_SIZE - CHUNK_OVERLAP):
            chunk = ' '.join(words[i:i+CHUNK_SIZE])
            if chunk:
                chunks.append(chunk)
        return chunks

    def embed_and_store(self, video_id, chunks):
        vectors = self.model.encode(chunks, show_progress_bar=False)
        self.faiss_service.add_video_embeddings(video_id, vectors, chunks)

    def semantic_search(self, video_id, question, top_k=3):
        question_vec = self.model.encode([question])
        return self.faiss_service.semantic_search(video_id, question_vec, top_k)

    def get_video_info(self, video_id):
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