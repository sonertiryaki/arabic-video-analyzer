from openpyxl import Workbook
from typing import List
import os


def create_excel(sentences: List[str], words: List[str], output_path: str) -> str:
    """
    2 sayfalı Excel oluşturur:
    - Cumleler
    - Kelimeler
    """

    wb = Workbook()

    # === CÜMLELER SAYFASI ===
    ws_sentences = wb.active
    ws_sentences.title = "Cumleler"
    ws_sentences.append(["No", "Cumle"])

    for idx, sentence in enumerate(sentences, start=1):
        ws_sentences.append([idx, sentence])

    # === KELİMELER SAYFASI ===
    ws_words = wb.create_sheet(title="Kelimeler")
    ws_words.append(["No", "Kelime"])

    for idx, word in enumerate(words, start=1):
        ws_words.append([idx, word])

    # === KAYDET ===
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)

    return output_path
