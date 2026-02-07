import pandas as pd
from camel_tools.utils.dediac import dediac_ar
from camel_tools.transliterate import Transliterator
from transformers import pipeline
from dictionary import load_dictionary, update_dictionary

translator = pipeline("translation", model="Helsinki-NLP/opus-mt-ar-tr")
tr = Transliterator('ar2bw')

def create_excel(text):

    words = list(set(text.split()))

    dict_df = load_dictionary()
    known_words = set(dict_df["Arabic"])

    results = []

    for w in words:

        clean = dediac_ar(w)
        translit = tr.transliterate(clean)
        meaning = translator(clean)[0]['translation_text']

        is_new = clean not in known_words

        results.append([clean, translit, meaning, is_new])

    update_dictionary(results)

    df = pd.DataFrame(results,
                      columns=["Arabic","Okunus","Turkce","NEW"])

    file = "analysis.xlsx"
    df.to_excel(file,index=False)

    return file
