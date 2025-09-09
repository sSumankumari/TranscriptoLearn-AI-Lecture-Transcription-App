from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq


class GroqService:
    def __init__(self):
        # Initialize Groq client
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Default to supported model, can be overridden via .env
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    def _safe_request(self, messages, max_tokens=1000, temperature=0.3):
        """
        Helper to safely call Groq API and return content.
        Handles missing/invalid responses gracefully.
        """
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            if response.choices and hasattr(response.choices[0].message, "content"):
                return response.choices[0].message.content.strip()
            return "⚠️ No response generated."
        except Exception as e:
            return f"⚠️ Groq API error: {str(e)}"

    def generate_notes(self, transcript, video_title):
        prompt = f"""
        Create comprehensive, well-structured study notes from this lecture transcript.

        Video Title: {video_title}

        Transcript: {transcript[:8000]}

        Please format the notes as follows:
        1. **Main Topic/Subject**
        2. **Key Concepts** (bullet points)
        3. **Important Definitions**
        4. **Examples and Applications**
        5. **Summary Points**

        Make the notes clear, concise, and suitable for studying.
        """
        return self._safe_request(
            [
                {"role": "system", "content": "You are an expert educational assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )

    def generate_summary(self, transcript):
        prompt = f"""
        Create a concise summary of this lecture in 5–7 paragraphs.
        Focus on the main points, key takeaways, and important concepts discussed.

        Transcript: {transcript[:6000]}
        """
        return self._safe_request(
            [
                {"role": "system", "content": "You are an expert at summarizing educational content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )

    def answer_question(self, context, question):
        prompt = f"""
        Based on the following transcript segments, answer this question clearly and accurately.
        If the answer is not in the transcript, say so.

        Question: {question}
        Transcript Segments: {context}
        """
        return self._safe_request(
            [
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
