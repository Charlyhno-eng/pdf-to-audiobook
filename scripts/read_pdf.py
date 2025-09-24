import os
import re
from PyPDF2 import PdfReader
from gtts import gTTS
from pydub import AudioSegment

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FOLDER = os.path.join(BASE_DIR, "input")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

PDF_FILENAME = "ainsi_parlait_zarathoustra.pdf"
PDF_PATH = os.path.join(INPUT_FOLDER, PDF_FILENAME)

OUTPUT_AUDIO_FILENAME = os.path.splitext(PDF_FILENAME)[0] + ".mp3"
OUTPUT_AUDIO_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_AUDIO_FILENAME)

EXCLUDED_PAGES = [1, 2, 3, 4, 5, 6, 7, 8]
LANGUAGE = "fr"

def read_pdf(file_path, excluded_pages=None):
    """Extracts text from a PDF file, skipping excluded pages."""
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

def clean_text(text):
    """Cleans up extracted text by removing unnecessary line breaks, extra spaces, and page numbers."""
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\d+\s', '', text)
    return text.strip()

def chunk_text(text, max_chars=4500):
    """Splits the text into chunks for gTTS, attempting to cut at sentence boundaries."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        if end < len(text):
            end = text.rfind('.', start, end)
            if end == -1:
                end = start + max_chars
        chunk = text[start:end+1].strip()
        if chunk:
            chunks.append(chunk)
        start = end + 1
    return chunks

def save_text_to_mp3(text, output_path, language="fr"):
    """Converts text to a single MP3 file using gTTS, merging chunks if necessary."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    chunks = chunk_text(text)

    temp_files = []
    for i, chunk in enumerate(chunks):
        temp_file = f"{output_path}_temp_{i}.mp3"
        tts = gTTS(text=chunk, lang=language)
        tts.save(temp_file)
        temp_files.append(temp_file)

    if len(temp_files) == 1:
        os.rename(temp_files[0], output_path)
    else:
        combined = AudioSegment.empty()

        for f in temp_files:
            combined += AudioSegment.from_file(f)
        combined.export(output_path, format="mp3")

        for f in temp_files:
            os.remove(f)

if __name__ == "__main__":
    print("PDF_PATH =", PDF_PATH)

    if os.path.exists(PDF_PATH):
        content = read_pdf(PDF_PATH, excluded_pages=EXCLUDED_PAGES)
        clean_content = clean_text(content)
        save_text_to_mp3(clean_content, OUTPUT_AUDIO_PATH, LANGUAGE)
        print("Conversion completed! Output:", OUTPUT_AUDIO_PATH)
    else:
        print("PDF not found.")
