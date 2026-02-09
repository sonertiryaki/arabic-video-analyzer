import re

# --------------------------------------------------
# ARAPÇA HAREKE TEMİZLEME
# --------------------------------------------------
ARABIC_DIACRITICS = re.compile(
    r"[\u064B-\u065F\u0670\u0640]"
)

def remove_diacritics(text: str) -> str:
    """
    Arapça harekeleri temizler
    """
    return re.sub(ARABIC_DIACRITICS, "", text)


# --------------------------------------------------
# ANALİZ ANA FONKSİYONU
# --------------------------------------------------
def analyze_video(video_name: str, drive_file_id: str):
    """
    Video analiz simülasyonu
    (Bir sonraki adımda OCR buraya bağlanacak)
    """

    print(f"🔍 Analiz başlatıldı: {video_name}")

    # --------------------------------------------------
    # ŞİMDİLİK SAHTE OCR ÇIKTISI
    # (Gerçek OCR sonraki adım)
    # --------------------------------------------------
    ocr_texts = [
        "إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ",
        "إِنَّ اللَّهَ غَفُورٌ رَحِيمٌ",
        "وَاللَّهُ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ",
        "اللَّهُ نُورُ السَّمَاوَاتِ وَالْأَرْضِ"
    ]

    results = []
    seen = set()

    for text in ocr_texts:
        normalized = remove_diacritics(text)

        # duplicate detection
        if normalized in seen:
            continue

        seen.add(normalized)

        results.append({
            "arabic": text,
            "arabic_normalized": normalized,
            "turkish": "Türkçe anlam daha sonra eklenecek"
        })

    print(f"✅ Analiz tamamlandı: {len(results)} benzersiz kayıt")

    return results
