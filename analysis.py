import os
import cv2
import pytesseract
import pandas as pd
import regex as re
from transformers import pipeline

# =====================================================
# TRANSLATOR (LAZY LOAD – STABLE)
# =====================================================
translator = None

def get_translator():
    global translator
    if translator is None:
        translator = pipeline(
            model="Helsinki-NLP/opus-mt-ar-tr"
        )
    return translator


# =====================================================
# ARABIC TEXT CLEAN
# =====================================================
def clean_arabic(text: str) -> str:
    # Unicode Arapça hareke + tatweel temizleme
    pattern = r"[\u064B-\u0652\u0670\u0640]"
    return re.sub(pattern, "", text).strip()


# =====================================================
# OCR FROM VIDEO (DUPLICATE FREE)
# =====================================================
def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)

    texts = set()
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_index += 1

        # Performans için her 20 frame
        if frame_index % 20 != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ocr_result = pytesseract.image_to_string(gray, lang="ara")

        for line in ocr_result.split("\n"):
            cleaned = clean_arabic(line)
            if len(cleaned) > 1:
                texts.add(cleaned)

    cap.release()
    return list(texts)


# =====================================================
# MAIN ANALYSIS
# =====================================================
def create_excel(video_path, output_dir):
    arabic_texts = extract_text_from_video(video_path)
    translator = get_translator()

    rows = []

    for ar in arabic_texts:
        try:
            tr = translator(ar)[0]["translation_text"]
        except Exception:
            tr = ""

        rows.append({
            "Arapça": ar,
            "Türkçe Anlam": tr
        })

    df = pd.DataFrame(rows)
    excel_path = os.path.join(output_dir, "analysis.xlsx")
    df.to_excel(excel_path, index=False)

    return excel_path
