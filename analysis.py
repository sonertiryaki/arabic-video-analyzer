import cv2
import pytesseract
import re
import os
from excel_writer import create_excel


# --------------------------------------------------
# ARAPÇA HAREKE TEMİZLEME (NET VE OKUNAKLI)
# --------------------------------------------------
ARABIC_DIACRITICS_PATTERN = re.compile(
    r"[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0640]"
)


def normalize_arabic(text: str) -> str:
    return re.sub(ARABIC_DIACRITICS_PATTERN, "", text).strip()


# --------------------------------------------------
# OCR SONUCU TEMİZLEME
# --------------------------------------------------
def clean_text(text: str) -> list:
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()
        if len(line) < 2:
            continue
        if not re.search(r"[\u0600-\u06FF]", line):
            continue
        cleaned.append(line)

    return cleaned


# --------------------------------------------------
# ANA ANALİZ FONKSİYONU
# --------------------------------------------------
def analyze_video(video_path: str, video_name: str):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("V
