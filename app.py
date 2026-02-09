from flask import Flask, request, jsonify
from analysis import analyze_video

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    return "Arabic Video Analyzer is running ✅", 200


@app.route("/process", methods=["POST"])
def process_video():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON body yok"}), 400

    video_name = data.get("video_name")
    drive_file_id = data.get("drive_file_id")

    if not video_name or not drive_file_id:
        return jsonify({"error": "video_name veya drive_file_id eksik"}), 400

    try:
        result = analyze_video(
            video_name=video_name,
            drive_file_id=drive_file_id
        )

        return jsonify({
            "status": "ok",
            "excel_path": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
