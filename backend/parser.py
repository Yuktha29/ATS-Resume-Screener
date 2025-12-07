# backend/parser.py
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Extract plain text from PDF using pdfplumber (100% compatible with macOS)."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""
    return text.strip()