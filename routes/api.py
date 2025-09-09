from flask import Blueprint, request, jsonify
from services.transcript_service import TranscriptService
from services.groq_service import GroqService
from utils.helpers import extract_video_id
import traceback

# Define Blueprint
api = Blueprint("api", __name__)

# Initialize services
transcript_service = TranscriptService()
groq_service = GroqService()


@api.route("/process-video", methods=["POST"])
def process_video():
    """Process a YouTube video to generate transcript, notes, and summary."""
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid request: JSON body required."}), 400

    video_url = data.get("url")
    if not video_url:
        return jsonify({"error": "No video URL provided."}), 400

    video_id = extract_video_id(video_url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL."}), 400

    try:
        # Fetch transcript
        transcript, transcript_list, transcript_language = transcript_service.get_transcript(video_id)

        # Chunk, embed, and store
        chunks = transcript_service.chunk_transcript(transcript)
        transcript_service.embed_and_store(video_id, chunks)

        # Get video info
        video_info = transcript_service.get_video_info(video_id)

        # Generate AI outputs
        notes = groq_service.generate_notes(transcript, video_info.get("title", video_id))
        summary = groq_service.generate_summary(transcript)

        return jsonify({
            "video_id": video_id,
            "video_info": video_info,
            "transcript": transcript,
            "transcript_language": transcript_language,
            "notes": notes,
            "summary": summary,
            "success": True,
            "source_url": f"https://www.youtube.com/watch?v={video_id}"
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        print("❌ Error in /process-video:", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@api.route("/ask-question", methods=["POST"])
def ask_question():
    """Answer user questions based on a processed video's transcript."""
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid request: JSON body required."}), 400

    video_id = data.get("video_id")
    question = data.get("question")

    if not video_id or not question:
        return jsonify({"error": "Both video_id and question are required."}), 400

    try:
        # Retrieve relevant transcript chunks
        relevant_chunks = transcript_service.semantic_search(video_id, question, top_k=3)

        if not relevant_chunks:
            return jsonify({
                "answer": "Sorry, I couldn't find relevant content for this video/question.",
                "success": False
            }), 200

        # Build context and query Groq
        context = "\n".join(relevant_chunks)
        answer = groq_service.answer_question(context, question)

        return jsonify({"answer": answer, "success": True})

    except Exception as e:
        print("❌ Error in /ask-question:", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@api.route("/health", methods=["GET"])
def health_check():
    """Check API health status."""
    return jsonify({
        "status": "healthy",
        "message": "TranscriptoLearn API is running"
    })
