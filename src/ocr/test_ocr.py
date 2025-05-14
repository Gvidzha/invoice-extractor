# src\ocr\test_ocr.py

import pytesseract
import sys
import os

#  Norādi pilnu ceļu uz tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Pievieno projekta saknes direktoriju Python ceļam
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.ocr.ocr_utils import extract_text_from_image

# Norādi attēla faila ceļu
image_path = r"C:\Users\User\Pictures\Screenshots\Ekrānuzņēmums 2025-05-11 115437.png"  # Norādi pilnu ceļu uz attēlu

# Izsauc funkciju un izdrukā rezultātu
extracted_text = extract_text_from_image(image_path)
print("Extracted Text:")
print(extracted_text)