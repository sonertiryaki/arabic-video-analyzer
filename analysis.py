import re
from transformers import pipeline

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ar-tr")

def normalize_arabic(text):
    text = re.sub("[ًٌٍَُِّْـ]", "", text)  # harekeleri kaldır
    return text

def simple_transliterate(word):
    return word  # şimdilik Arapça 그대로 bırakıyoruz
