import cv2
import pytesseract
import re
from typing import List, Set

# Tesseract Arapça dili
TESSERACT_LANG = "ara"

# HAREKE TEMIZLEME REGEX'I
ARABIC_DIACRITICS = re.compile(r"[ًٌٍَُِّْـ]")

def clean_arabic_text(text: str) -> str:
    """
    Arapça metinden:
    - Harekeleri
    - Fazla boşlukları
    - Geçersiz karakterleri temizler
    """
    text = ARABIC_DIACRITICS.sub("", text)
    text = re.sub(r"[^\u0600-\u06FF\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_from_video(
    video_path: str,
    frame_interval: int = 30
) -> List[str]:
    """
    Videodan frame alır, OCR uygular ve
    TEKRARSIZ cümle listesi döner
    """

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Video açılamadı")

    extracted_sentences: Set[str] = set()
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Her N frame'de bir OCR
        if frame_count % frame_interval != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        ocr_text = pytesseract.image_to_string(
            gray,
            lang=TESSERACT_LANG,
            config="--psm 6"
        )

        for line in ocr_text.splitlines():
            cleaned = clean_arabic_text(line)

            # Çok kısa ve anlamsız şeyleri at
            if len(cleaned) < 4:
                continue

            extracted_sentences.add(cleaned)

    cap.release()

    return sorted(extracted_sentences)
