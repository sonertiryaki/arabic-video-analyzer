from flask import Flask, request, jsonify
import os
from analysis import analyze_video

app = Flask(__name__)

UPLOAD_DIR = "/tmp"


@app.route("/", methods=["GET"])
def health():
    return "Arabic Video Analyzer is running", 200


@app.route("/process", methods=["POST"])
def process_video():
    if "video" not in request.files:
        return jsonify({"error": "Video file not found"}), 400

    video_file = request.files["video"]
    video_name = request.form.get("video_name", video_file.filename)

    if not video_name:
        return jsonify({"error": "Video name missing"}), 400

    video_path = os.path.join(UPLOAD_DIR, video_name)
    video_file.save(video_path)

    try:
        excel_path = analyze_video(video_path, video_name)

        return jsonify({
            "status": "success",
            "video": video_name,
            "excel": excel_path
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
