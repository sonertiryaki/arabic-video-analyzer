import os
import cv2
import pytesseract
import re
from excel_writer import write_excel


TEMP_DIR = "temp"
OUTPUT_DIR = "output"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def analyze_video(video_name: str, drive_file_id: str) -> str:
    """
    Ana analiz fonksiyonu
    """
    video_path = download_video_stub(video_name)
    frames_text = extract_text_from_video(video_path)

    cleaned = clean_and_deduplicate(frames_text)

    excel_path = write_excel(
        video_name=video_name,
        rows=cleaned
    )

    return excel_path


# --------------------------------------------------
# VIDEO INDIRME (SIMDI STUB)
# --------------------------------------------------

def download_video_stub(video_name: str) -> str:
    """
    Şimdilik video indirme yok.
    Render tarafında test için boş video path döndürür.
    """
    fake_path = os.path.join(TEMP_DIR, video_name)
    open(fake_path, "a").close()
    return fake_path


# --------------------------------------------------
# VIDEO -> OCR
# --------------------------------------------------

def extract_text_from_video(video_path: str):
    """
    Videodan belirli aralıklarla frame alıp OCR uygular
    """
    cap = cv2.VideoCapture(video_path)
    texts = []

    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Her 30 frame'de bir OCR
        if frame_index % 30 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(
                gray,
                lang="ara"
            )
            if text.strip():
                texts.append(text)

        frame_index += 1

    cap.release()
    return texts


# --------------------------------------------------
# TEMIZLIK + DUPLICATE
# --------------------------------------------------

def clean_and_deduplicate(texts):
    """
    - Harekeleri temizler
    - Satır bazlı böler
    - Tekrar edenleri siler
    """
    seen = set()
    rows = []

    for block in texts:
        lines = block.splitlines()

        for line in lines:
            line = normalize_arabic(line)

            if not line:
                continue

            if line in seen:
                continue

            seen.add(line)
