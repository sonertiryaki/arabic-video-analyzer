import os
from flask import Flask, request

from drive import (
    prepare_video_folder,
    download_video_from_request,
    upload_result,
    already_processed,
    mark_processed
)
from video import extract_frames
from ocr import run_ocr
from analysis import create_excel
from mail import send_mail


app = Flask(__name__)


@app.route("/process", methods=["POST"])
def process():
    """
    Apps Script'ten gelen videoyu alır,
    analiz eder ve sonucu hazırlar.
    """

    # 1. Videoyu kaydet
    video_file = download_video_from_request(request)

    # 2. Video adına göre klasör oluştur
    folder_name, filename = prepare_video_folder(video_file)

    # 3. Daha önce işlendi mi kontrol et
    if already_processed(folder_name):
        return "already processed", 200

    # 4. Videodan frame çıkar
    frames = extract_frames(video_file)

    # 5. OCR ile metni oku
    text = run_ocr(frames)

    # 6. Analiz & Excel oluştur
    report_file = create_excel(text)

    # 7. Excel’i klasöre taşı
    upload_result(report_file, folder_name)

    # 8. İşlendi olarak işaretle
    mark_processed(folder_name)

    # 9. Bildirim (şimdilik console)
    send_mail(f"{filename} analizi tamamlandı")

    return "ok", 200


# -------------------------------------------------
# RENDER / FLASK PORT BINDING (ÇOK KRİTİK)
# -------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
