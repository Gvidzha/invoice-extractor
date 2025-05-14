# src/ocr/ocr_utils.py
import pytesseract
from PIL import Image

# Norāda pilnu ceļu uz tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image, report_file="ocr_report.txt"):
    """
    Šī funkcija izmanto Tesseract OCR, lai izvilktu tekstu no attēla objekta.
    Tā arī saglabā atskaites par atpazīšanas precizitāti.
    """
    # Pārliecinieties, ka attēls ir PIL.Image objekts
    if not isinstance(image, Image.Image):
        raise ValueError("Input must be a PIL.Image object")

    # Iegūst tekstu no attēla, izmantojot latviešu valodu
    extracted_text = pytesseract.image_to_string(image, lang='lat')

    # Iegūst informāciju par atpazītajiem simboliem
    boxes = pytesseract.image_to_boxes(image, lang='lat')
    recognized_characters = len(boxes.splitlines())

    # Iegūst kopējo simbolu skaitu attēlā (aptuveni)
    total_characters = image.size[0] * image.size[1] // 1000  # Piemēram, 1 simbols uz 1000 pikseļiem

    # Aprēķina procentuālo atpazīšanas precizitāti
    recognition_percentage = (recognized_characters / total_characters) * 100 if total_characters > 0 else 0

    # Saglabā atskaiti failā
    with open(report_file, "a", encoding="utf-8") as report:
        report.write(f"Atpazīto simbolu skaits: {recognized_characters}\n")
        report.write(f"Kopējais simbolu skaits (aptuveni): {total_characters}\n")
        report.write(f"Atpazīšanas precizitāte: {recognition_percentage:.2f}%\n")
        report.write("-" * 40 + "\n")

    return extracted_text
