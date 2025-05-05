import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for i, page in enumerate(doc):
        page_text = page.get_text()
        text += f"\n--- Page {i + 1} ---\n"
        text += page_text
    doc.close()
    return text