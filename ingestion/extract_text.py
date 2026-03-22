from __future__ import annotations

import fitz  # PyMuPDF
from tqdm import tqdm

from utils.config import RAW_DIR, PROCESSED_DIR
from utils.file_io import save_json


def extract_pdf_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        pages.append(
            {
                "source_file": pdf_path.name,
                "page_number": page_num + 1,
                "text": text.strip(),
            }
        )

    return pages


def main():
    pdf_files = list(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in {RAW_DIR}")
        return

    for pdf_path in tqdm(pdf_files, desc="Extracting PDFs"):
        extracted_pages = extract_pdf_pages(pdf_path)

        output_path = PROCESSED_DIR / f"{pdf_path.stem}.json"
        save_json(extracted_pages, output_path)

        print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()