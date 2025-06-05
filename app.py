from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
import re
from groq import Groq
import json
import logging
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))


class TranscriptProcessor:
    def __init__(self):
        self.transcripts = {}

    def extract_video_id(self, url):
        """Extract YouTube video ID from URL"""
        try:
            parsed_url = urlparse(url)
            if 'youtube.com' in parsed_url.netloc:
                return parse_qs(parsed_url.query)['v'][0]
            elif 'youtu.be' in parsed_url.netloc:
                return parsed_url.path[1:]
            else:
                raise ValueError("Invalid YouTube URL")
        except Exception as e:
            logger.error(f"Error extracting video ID: {str(e)}")
            return None

    def get_video_info(self, video_id):
        """Get video title and duration using yt-dlp"""
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
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return {'title': 'Unknown Title', 'duration': 0, 'uploader': 'Unknown'}

    def get_transcript(self, video_id):
        """Extract transcript from YouTube video"""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_transcript = ' '.join([entry['text'] for entry in transcript_list])

            # Store transcript with timestamps for Q&A
            self.transcripts[video_id] = {
                'full_text': full_transcript,
                'timestamped': transcript_list
            }

            return full_transcript
        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            raise Exception(f"Could not retrieve transcript: {str(e)}")

    def generate_notes(self, transcript, video_title):
        """Generate structured notes using Groq API"""
        try:
            prompt = f"""
            Create comprehensive, well-structured study notes from this lecture transcript.

            Video Title: {video_title}

            Transcript: {transcript[:8000]}  # Limit to avoid token limits

            Please format the notes as follows:
            1. **Main Topic/Subject**
            2. **Key Concepts** (bullet points)
            3. **Important Definitions** 
            4. **Examples and Applications**
            5. **Summary Points**

            Make the notes clear, concise, and suitable for studying.
            """

            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": "You are an expert educational assistant that creates clear, structured study notes from lecture content."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=2000
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating notes: {str(e)}")
            raise Exception(f"Could not generate notes: {str(e)}")

    def generate_summary(self, transcript):
        """Generate a concise summary using Groq API"""
        try:
            prompt = f"""
            Create a concise summary of this lecture in 3-4 paragraphs.
            Focus on the main points, key takeaways, and important concepts discussed.

            Transcript: {transcript[:6000]}
            """

            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": "You are an expert at summarizing educational content clearly and concisely."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=1000
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Summary could not be generated."

    def answer_question(self, video_id, question):
        """Answer questions about the video content"""
        if video_id not in self.transcripts:
            return "Please process a video first before asking questions."

        transcript = self.transcripts[video_id]['full_text']

        try:
            prompt = f"""
            Based on the following lecture transcript, answer this question clearly and accurately.
            If the answer is not in the transcript, say so.

            Question: {question}

            Transcript: {transcript[:6000]}
            """

            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system",
                     "content": "You are a helpful educational assistant. Answer questions based only on the provided transcript content."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192",
                temperature=0.3,
                max_tokens=1000
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return "Sorry, I couldn't process your question at the moment."


# Initialize processor
processor = TranscriptProcessor()


@app.route('/api/process-video', methods=['POST'])
def process_video():
    try:
        data = request.get_json()
        video_url = data.get('url')

        if not video_url:
            return jsonify({'error': 'No video URL provided'}), 400

        # Extract video ID
        video_id = processor.extract_video_id(video_url)
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        # Get video information
        video_info = processor.get_video_info(video_id)

        # Get transcript
        transcript = processor.get_transcript(video_id)

        # Generate notes and summary
        notes = processor.generate_notes(transcript, video_info['title'])
        summary = processor.generate_summary(transcript)

        return jsonify({
            'video_id': video_id,
            'video_info': video_info,
            'transcript': transcript,
            'notes': notes,
            'summary': summary,
            'success': True
        })

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        video_id = data.get('video_id')
        question = data.get('question')

        if not video_id or not question:
            return jsonify({'error': 'Video ID and question are required'}), 400

        answer = processor.answer_question(video_id, question)

        return jsonify({
            'answer': answer,
            'success': True
        })

    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'TranscriptoLearn API is running'})


if __name__ == '__main__':
    # Check if Groq API key is set
    if not os.getenv('GROQ_API_KEY'):
        logger.error("GROQ_API_KEY not found in environment variables")
        print("Please set your GROQ_API_KEY in the .env file")
    else:
        print("Starting TranscriptoLearn API...")
        app.run(debug=True, host='0.0.0.0', port=5000)