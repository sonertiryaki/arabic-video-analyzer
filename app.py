import os
from flask import Flask, request, jsonify
from analysis import create_excel

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health():
    return "Arabic Video Analyzer is running", 200


@app.route("/process", methods=["POST"])
def process_video():
    """
    Beklenen JSON:
    {
        "video_path": "/opt/render/project/src/video.mp4",
        "output_dir": "/opt/render/project/src/output"
    }
    """

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body missing"}), 400

    video_path = data.get("video_path")
    output_dir = data.get("output_dir")

    if not video_path or not output_dir:
        return jsonify({"error": "video_path or output_dir missing"}), 400

    if not os.path.exists(video_path):
        return jsonify({"error": "Video not found"}), 404

    os.makedirs(output_dir, exist_ok=True)

    excel_path = create_excel(video_path, output_dir)

    return jsonify({
        "status": "ok",
        "excel_file": excel_path
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
