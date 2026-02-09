import os
import json
from flask import Flask, request, jsonify

from analysis import analyze_video
from excel_writer import write_excel

app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return "Arabic Video Analyzer is running ✅", 200


@app.route("/process", methods=["POST"])
def process_video():
    try:
        data = request.get_json(force=True)

        video_name = data.get("video_name")
        drive_file_id = data.get("drive_file_id")

        if not video_name or not drive_file_id:
            return jsonify({
                "status": "error",
                "message": "video_name veya drive_file_id eksik"
            }), 400

        print(f"🎬 Video alındı: {video_name}")
        print(f"📁 Drive File ID: {drive_file_id}")

        # --------------------------------------------------
        # ŞİMDİLİK: Video işleme simülasyonu
        # Bir sonraki adımda Drive'dan indirme eklenecek
        # --------------------------------------------------

        analysis_result = analyze_video(
            video_name=video_name,
            drive_file_id=drive_file_id
        )

        excel_path = write_excel(
            video_name=video_name,
            analysis_result=analysis_result
        )

        return jsonify({
            "status": "success",
            "video": video_name,
            "excel_file": excel_path
        }), 200

    except Exception as e:
        print("❌ HATA:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
