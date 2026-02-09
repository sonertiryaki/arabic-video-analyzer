from typing import List, Tuple
from ocr import extract_text_from_video


def extract_words_from_sentences(sentences: List[str]) -> List[str]:
    """
    Cümle listesinden TEKRARSIZ kelime listesi çıkarır
    """
    words_set = set()

    for sentence in sentences:
        for word in sentence.split():
            if len(word) < 2:
                continue
            words_set.add(word)

    return sorted(words_set)


def analyze_video(video_path: str) -> Tuple[List[str], List[str]]:
    """
    Video analizinin ana fonksiyonu

    DÖNER:
    - cümleler (tekrarsız)
    - kelimeler (tekrarsız)
    """

    sentences = extract_text_from_video(video_path)
    words = extract_words_from_sentences(sentences)

    return sentences, words
