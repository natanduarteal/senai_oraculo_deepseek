import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

def pdf_reader(path):
    
    total_text=""

    try:
        reader=PdfReader(path)
        for page in reader.pages:
            content=page.extract_text()
            if content:
                total_text+=content+ "\n"


        if len(total_text.strip())<100:
            print("applying OCR")
            images=convert_from_path(path)
            for img in images:
                text_ocr=pytesseract.image_to_string(img,lang="por")
                total_text+=text_ocr + "\n"
    except Exception as e:
        print(f"failed to read {path}: {e}")
    return total_text        