# src\ocr\generate_ocr_texts.py

import os
import sys
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError
from PIL import Image  # Importē Image, lai atvērtu attēlus

# Pievieno projekta saknes direktoriju Python ceļam
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.ocr.ocr_utils import extract_text_from_image

# Ceļi uz datu direktorijām
raw_dir = "data/raw"
ocr_texts_dir = "data/ocr_texts"

# Izveido OCR tekstu direktoriju, ja tāda nav
os.makedirs(ocr_texts_dir, exist_ok=True)

# Funkcija PDF apstrādei
def process_pdf(pdf_path):
    try:
        # Norādiet pilnu ceļu uz Poppler `bin` direktoriju
        poppler_path = r"C:\Program Files\poppler-24.08.0\Library\bin"
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        text = ""
        for i, image in enumerate(images):
            # Izgūst tekstu no katras PDF lapas, nododot attēla objektu
            page_text = extract_text_from_image(image)
            text += page_text + "\n"
        return text
    except PDFInfoNotInstalledError:
        print("Error: Poppler is not installed or not in PATH. Please install Poppler and ensure it is accessible.")
        sys.exit(1)

# Apstrādā visus failus no `data/raw`
for file_name in os.listdir(raw_dir):
    file_path = os.path.join(raw_dir, file_name)

    # Apstrādā attēlu failus
    if file_name.endswith((".png", ".jpg", ".jpeg")):
        # Atver attēlu un nodod to extract_text_from_image
        with Image.open(file_path) as image:
            ocr_text = extract_text_from_image(image)
        ocr_text_file = os.path.join(ocr_texts_dir, f"{os.path.splitext(file_name)[0]}.txt")
        with open(ocr_text_file, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        print(f"OCR teksts saglabāts: {ocr_text_file}")

    # Apstrādā PDF failus
    elif file_name.endswith(".pdf"):
        ocr_text = process_pdf(file_path)
        ocr_text_file = os.path.join(ocr_texts_dir, f"{os.path.splitext(file_name)[0]}.txt")
        with open(ocr_text_file, "w", encoding="utf-8") as f:
            f.write(ocr_text)
        print(f"OCR teksts no PDF saglabāts: {ocr_text_file}")