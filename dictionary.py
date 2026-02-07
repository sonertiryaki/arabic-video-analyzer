import pandas as pd
import os

DICT_FILE = "dictionary.xlsx"

def load_dictionary():

    if os.path.exists(DICT_FILE):
        return pd.read_excel(DICT_FILE)

    else:
        df = pd.DataFrame(columns=["Arabic","Okunus","Turkce"])
        df.to_excel(DICT_FILE,index=False)
        return df

def update_dictionary(new_words):

    df = load_dictionary()

    existing = set(df["Arabic"])

    new_entries = []

    for row in new_words:
        if row[0] not in existing:
            new_entries.append(row)

    if len(new_entries) > 0:
        df2 = pd.DataFrame(new_entries,
                           columns=["Arabic","Okunus","Turkce"])
        df = pd.concat([df, df2])
        df.to_excel(DICT_FILE,index=False)

    return existing
