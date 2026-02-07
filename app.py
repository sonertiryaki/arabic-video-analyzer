from flask import Flask, request
from drive import prepare_video_folder, download_video, upload_result, already_processed, mark_processed
from video import extract_frames
from ocr import run_ocr
from analysis import create_excel
from mail import send_mail

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process():

    file_id = request.json["fileId"]

    folder_id, filename = prepare_video_folder(file_id)

    if already_processed(folder_id):
        return "already processed"

    video = download_video(file_id)
    frames = extract_frames(video)

    text = run_ocr(frames)

    report = create_excel(text)

    upload_result(report, folder_id)

    mark_processed(folder_id)

    send_mail(filename + " analiz edildi")

    return "ok"

if __name__ == "__main__":
    app.run()
