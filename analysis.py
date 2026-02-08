import re
import pandas as pd
from transformers import pipeline
from dictionary import load_dictionary, update_dictionary


# -----------------------------
# ARAPÇA NORMALİZASYON
# -----------------------------
def normalize_arabic(text: str) -> str:
    """
    Arapça harekeleri ve uzatma çizgisini kaldırır.
    Örnek:
    كِتَابٌ → كتاب
    """
    arabic_diacritics = re.compile(r'[\u064B-\u0652\u0640]')
    return re.sub(arabic_diacritics, '', text)


# -----------------------------
# BASİT TRANSLITERATION (PURE PYTHON)
# -----------------------------
ARABIC_TO_LATIN = {
    'ا': 'a', 'ب': 'b', 'ت': 't', 'ث': 'th',
    'ج': 'j', 'ح': 'h', 'خ': 'kh',
    'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z',
    'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd',
    'ط': 't', 'ظ': 'z', 'ع': '‘', 'غ': 'gh',
    'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l',
    'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w',
    'ي': 'y', 'ء': '', 'ى': 'a', 'ة': 'h'
}

def transliterate(word: str) -> str:
    """
    Basit Arapça → Latin okunuş üretir.
    """
    return ''.join(ARABIC_TO_LATIN.get(ch, ch) for ch in word)


# -----------------------------
# ÇEVİRİ MODELİ (ÜCRETSİZ)
# -----------------------------
translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-ar-tr"
)


# -----------------------------
# ANA ANALİZ FONKSİYONU
# -----------------------------
def create_excel(text: str) -> str:

    # kelimeleri ayıkla + duplicate temizle
    raw_words = set(text.split())

    dictionary_df = load_dictionary()
    known_words = set(dictionary_df["Arabic"])

    results = []

    for word in raw_words:

        clean = normalize_arabic(word)

        if len(clean) < 2:
            continue

        try:
            meaning = translator(clean)[0]["translation_text"]
        except Exception:
            meaning = ""

        okunus = transliterate(clean)
        is_new = clean not in known_words

        results.append([
            clean,
            okunus,
            meaning,
            is_new
        ])

    # merkezi sözlüğü güncelle
    update_dictionary(results)

    df = pd.DataFrame(
        results,
        columns=["Arabic", "Okunus", "Turkce", "NEW"]
    )

    output_file = "analysis.xlsx"
    df.to_excel(output_file, index=False)

    return output_file
