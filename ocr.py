import pytesseract

def run_ocr(frames):

    text_set = set()

    for f in frames:
        txt = pytesseract.image_to_string(f, lang="ara")
        lines = txt.split("\n")

        for l in lines:
            clean = l.strip()
            if len(clean) > 1:
                text_set.add(clean)

    return "\n".join(text_set)
