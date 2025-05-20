# src/ocr/ocr_utils.py
import pytesseract
from PIL import Image, ImageEnhance

# Norāda pilnu ceļu uz tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image, report_file="ocr_report.txt"):
    """
    Šī funkcija izmanto Tesseract OCR, lai izvilktu tekstu no attēla objekta.
    Tā arī uzlabo attēlu un saglabā atskaites par atpazīšanas precizitāti.
    """
    if not isinstance(image, Image.Image):
        raise ValueError("Input must be a PIL.Image object")

    # Konvertē uz pelēko skalu
    image = image.convert('L')

    # Uzlabo kontrastu
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Palielina izmēru (piemēram, 2x)
    width, height = image.size
    image = image.resize((width * 2, height * 2))

    # Atpazīst tekstu
    extracted_text = pytesseract.image_to_string(image, lang='lav')

    # Simbolu info
    boxes = pytesseract.image_to_boxes(image, lang='lav')
    recognized_characters = len(boxes.splitlines())
    total_characters = image.size[0] * image.size[1] // 1000
    recognition_percentage = (recognized_characters / total_characters) * 100 if total_characters > 0 else 0

    # Atskaites saglabāšana
    with open(report_file, "a", encoding="utf-8") as report:
        report.write(f"Atpazīto simbolu skaits: {recognized_characters}\n")
        report.write(f"Kopējais simbolu skaits (aptuveni): {total_characters}\n")
        report.write(f"Atpazīšanas precizitāte: {recognition_percentage:.2f}%\n")
        report.write("-" * 40 + "\n")

    return extracted_text
