import os
from PyPDF2 import PdfReader
from gtts import gTTS

# ===== Constants =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

PDF_FILENAME = "ainsi_parlait_zarathoustra.pdf"
PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILENAME)

OUTPUT_AUDIO_FILENAME = os.path.splitext(PDF_FILENAME)[0] + ".mp3"
OUTPUT_AUDIO_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_AUDIO_FILENAME)

EXCLUDED_PAGES = [1,2,3,4,5,6,7,8]

LANGUAGE = "fr"

# ===== Functions =====
def read_pdf(file_path, excluded_pages=None):
    reader = PdfReader(file_path)
    text = ""
    for i, page in enumerate(reader.pages):
        page_number = i + 1
        if excluded_pages and page_number in excluded_pages:
            continue
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def save_text_to_mp3(text, output_path, language="fr"):
    tts = gTTS(text=text, lang=language)
    tts.save(output_path)

# ===== Main =====
if __name__ == "__main__":
    if os.path.exists(PDF_PATH):
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        content = read_pdf(PDF_PATH, excluded_pages=EXCLUDED_PAGES)
        save_text_to_mp3(content, OUTPUT_AUDIO_PATH, LANGUAGE)
