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

    # video dosyasını kaydet
    video_file = download_video_from_request(request)

    folder_name, filename = prepare_video_folder(video_file)

    if already_processed(folder_name):
        return "already processed"

    frames = extract_frames(video_file)
    text = run_ocr(frames)

    report = create_excel(text)

    upload_result(report, folder_name)
    mark_processed(folder_name)

    send_mail(f"{filename} analiz edildi")

    return "ok"

if __name__ == "__main__":
    app.run()
