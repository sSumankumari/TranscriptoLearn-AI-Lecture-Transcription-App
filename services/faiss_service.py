import os
import faiss
import numpy as np
import json

EMBEDDINGS_DIR = "embeddings"

class FAISSService:
    def __init__(self, dim):
        self.dim = dim
        os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

    def create_index(self, vectors):
        """Create a new FAISS index from a numpy array of vectors."""
        index = faiss.IndexFlatL2(self.dim)
        index.add(vectors.astype('float32'))
        return index

    def save_index(self, video_id, index):
        """Save the FAISS index to disk."""
        faiss.write_index(index, os.path.join(EMBEDDINGS_DIR, f"{video_id}.index"))

    def load_index(self, video_id):
        """Load a FAISS index from disk."""
        index_path = os.path.join(EMBEDDINGS_DIR, f"{video_id}.index")
        if os.path.exists(index_path):
            return faiss.read_index(index_path)
        return None

    def save_chunks(self, video_id, chunks):
        """Save chunked transcript text to disk."""
        with open(os.path.join(EMBEDDINGS_DIR, f"{video_id}_chunks.json"), "w", encoding="utf-8") as f:
            json.dump(chunks, f)

    def load_chunks(self, video_id):
        """Load chunked transcript text from disk."""
        chunks_path = os.path.join(EMBEDDINGS_DIR, f"{video_id}_chunks.json")
        if os.path.exists(chunks_path):
            with open(chunks_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def add_video_embeddings(self, video_id, vectors, chunks):
        """Create and save both FAISS index and chunk metadata for a video."""
        index = self.create_index(vectors)
        self.save_index(video_id, index)
        self.save_chunks(video_id, chunks)

    def semantic_search(self, video_id, query_vector, top_k=3):
        """Search for top_k most similar chunks for a question embedding."""
        index = self.load_index(video_id)
        chunks = self.load_chunks(video_id)
        if index is None or chunks is None:
            return []
        D, I = index.search(np.array(query_vector).astype('float32'), top_k)
        return [chunks[i] for i in I[0]]
