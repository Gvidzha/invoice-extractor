import os
import json

# OCR tekstu direktorija
ocr_texts_dir = "data/ocr_texts"
annotations_file = "data/annotations.json"

# Iegūst visus OCR tekstu failus
ocr_files = [f for f in os.listdir(ocr_texts_dir) if f.endswith(".txt")]

annotations = []

for ocr_file in ocr_files:
    file_path = os.path.join(ocr_texts_dir, ocr_file)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Izveido tokens no teksta
    tokens = content.split()
    
    # Noklusējuma labels (visi "O")
    labels = ["O"] * len(tokens)
    
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
