from flask import Blueprint, request, jsonify
from services.transcript_service import TranscriptService
from services.groq_service import GroqService
from utils.helpers import extract_video_id

api = Blueprint('api', __name__)
transcript_service = TranscriptService()
groq_service = GroqService()

@api.route('/process-video', methods=['POST'])
def process_video():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid request: JSON body required.'}), 400

    video_url = data.get('url')
    if not video_url:
        return jsonify({'error': 'No video URL provided'}), 400
    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    try:
        transcript, transcript_list, transcript_language = transcript_service.get_transcript(video_id)
        chunks = transcript_service.chunk_transcript(transcript)
        transcript_service.embed_and_store(video_id, chunks)
        video_info = transcript_service.get_video_info(video_id)

        notes = groq_service.generate_notes(transcript, video_info.get('title', video_id))
        summary = groq_service.generate_summary(transcript)
        return jsonify({
            'video_id': video_id,
            'video_info': video_info,
            'transcript': transcript,
            'transcript_language': transcript_language,
            'notes': notes,
            'summary': summary,
            'success': True,
            'source_url': f"https://www.youtube.com/watch?v={video_id}"
        })
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 404
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred while processing the video.'}), 500

@api.route('/ask-question', methods=['POST'])
def ask_question():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid request: JSON body required.'}), 400

    video_id = data.get('video_id')
    question = data.get('question')
    if not video_id or not question:
        return jsonify({'error': 'Video ID and question are required'}), 400
    try:
        relevant_chunks = transcript_service.semantic_search(video_id, question, top_k=3)
        if not relevant_chunks:
            return jsonify({'answer': "Sorry, couldn't find relevant content for this video/question."}), 200
        context = "\n".join(relevant_chunks)
        answer = groq_service.answer_question(context, question)
        return jsonify({'answer': answer, 'success': True})
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred while answering the question.'}), 500

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'TranscriptoLearn API is running'})