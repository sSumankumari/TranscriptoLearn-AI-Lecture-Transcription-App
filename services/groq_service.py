from dotenv import load_dotenv
load_dotenv()
import os
from groq import Groq

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))

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
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert educational assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=2000
        )
        return response.choices[0].message.content

    def generate_summary(self, transcript):
        prompt = f"""
        Create a concise summary of this lecture in 5-7 paragraphs.
        Focus on the main points, key takeaways, and important concepts discussed.
        Transcript: {transcript[:6000]}
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert at summarizing educational content."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content

    def answer_question(self, context, question):
        prompt = f"""
        Based on the following transcript segments, answer this question clearly and accurately.
        If the answer is not in the transcript, say so.
        Question: {question}
        Transcript Segments: {context}
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful educational assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            temperature=0.3,
            max_tokens=1000
        )
        return response.choices[0].message.content