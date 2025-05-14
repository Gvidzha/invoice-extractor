# src\utils\auto_labeler.py

import os
import json
import re

# OCR tekstu direktorija un anotāciju fails
ocr_texts_dir = "data/ocr_texts"
annotations_file = "data/annotations.json"

# Noteikumi un regulārās izteiksmes labels piešķiršanai
rules = {
    "B-DATE": r"\b\d{4}-\d{2}-\d{2}\b",  # Datums formātā YYYY-MM-DD
    "B-TOTAL": r"\b(?:kopā|summa|apmaksai)\b",  # Kopējā summa
    "B-ORGANIZATION": r"\b(?:SIA|AS|Ltd|Inc)\b",  # Organizācijas nosaukumi
    "B-LOCATION": r"\b(?:Rīga|Liepāja|Latvija|LV-\d{4})\b",  # Vietas nosaukumi
    "B-Amount": r"\b\d+,\d{2}\b",  # Naudas summas (ar komatu)
}

def auto_label_tokens(tokens):
    """
    Automātiski piešķir labels tokeniem, pamatojoties uz noteikumiem.
    """
    labels = ["O"] * len(tokens)  # Noklusējuma labels ir "O"
    for i, token in enumerate(tokens):
        for label, pattern in rules.items():
            if re.match(pattern, token):
                labels[i] = label
                break  # Pārtrauc, ja atrasts atbilstošs labels
    return labels

def process_ocr_texts():
    """
    Apstrādā OCR tekstus un ģenerē anotācijas ar automātiski piešķirtiem labels.
    """
    annotations = []
    ocr_files = [f for f in os.listdir(ocr_texts_dir) if f.endswith(".txt")]

    for ocr_file in ocr_files:
        file_path = os.path.join(ocr_texts_dir, ocr_file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Izveido tokens no teksta
        tokens = content.split()

        # Automātiski piešķir labels
        labels = auto_label_tokens(tokens)

        # Pievieno anotāciju
        annotations.append({
            "file": ocr_file,
            "tokens": tokens,
            "labels": labels
        })

    # Saglabā anotācijas failā
    with open(annotations_file, "w", encoding="utf-8") as f:
        json.dump(annotations, f, indent=4, ensure_ascii=False)

    print(f"Anotācijas saglabātas failā: {annotations_file}")




if __name__ == "__main__":
    process_ocr_texts()
