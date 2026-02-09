from flask import Flask, request, jsonify
import os
import tempfile

from ocr import extract_text_from_video
from analysis import analyze_text
from excel_writer import write_excel

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    return "Arabic Video Analyzer is running ✅", 200


@app.route("/process", methods=["POST"])
def process_video():
    try:
        data = request.get_json()

        video_name = data.get("video_name")
        drive_file_id = data.get("drive_file_id")

        if not video_name or not drive_file_id:
            return jsonify({"error": "Eksik parametre"}), 400

        # Şimdilik video download yok (ileride eklenecek)
        # OCR + analiz pipeline'ı simüle metinle başlatıyoruz
        # (Drive download ekleyince burası gerçek video olacak)

        print(f"📥 Video alındı: {video_name}")

        # ÖRNEK METİN (şimdilik)
        raw_text = extract_text_from_video(None)

        # Analiz
        analysis_result = analyze_text(raw_text)

        # Excel yaz
        output_dir = tempfile.mkdtemp()
        excel_path = os.path.join(
            output_dir, f"{video_name}_analysis.xlsx"
        )

        write_excel(analysis_result, excel_path)

        print(f"📊 Excel oluşturuldu: {excel_path}")

        return jsonify({
            "status": "success",
            "video": video_name,
            "excel": excel_path
        }), 200

    except Exception as e:
        print("❌ HATA:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
