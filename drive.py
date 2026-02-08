import os
import shutil


def prepare_video_folder(filename: str):
    """
    Video adıyla yerel bir klasör oluşturur.
    Örnek:
    video.mp4 → video/
    """
    folder_name = os.path.splitext(filename)[0]

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    return folder_name, filename


def download_video_from_request(request):
    """
    Apps Script'ten gelen video bytes'ını kaydeder.
    """
    filename = request.headers.get("filename", "video.mp4")

    with open(filename, "wb") as f:
        f.write(request.data)

    return filename


def upload_result(file_path: str, folder_name: str):
    """
    Analiz dosyasını ilgili klasöre taşır.
    """
    shutil.move(file_path, os.path.join(folder_name, file_path))


def mark_processed(folder_name: str):
    """
    Aynı videonun tekrar işlenmemesi için işaret dosyası oluşturur.
    """
    with open(os.path.join(folder_name, "processed.txt"), "w") as f:
        f.write("processed")


def already_processed(folder_name: str) -> bool:
    """
    Video daha önce işlendi mi?
    """
    return os.path.exists(os.path.join(folder_name, "processed.txt"))
