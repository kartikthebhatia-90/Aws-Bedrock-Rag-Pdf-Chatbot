from pathlib import Path

from tqdm import tqdm

from utils.config import PROCESSED_DIR, CHUNKS_DIR
from utils.file_io import load_json, save_json


def chunk_words(text: str, chunk_size: int = 200, overlap: int = 50):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start += chunk_size - overlap

    return chunks


def process_file(json_path: Path):
    data = load_json(json_path)
    all_chunks = []
    chunk_id = 1

    for page in data:
        page_text = page["text"]
        page_chunks = chunk_words(page_text, chunk_size=200, overlap=50)

        for chunk_text in page_chunks:
            all_chunks.append(
                {
                    "chunk_id": f"{json_path.stem}_chunk_{chunk_id}",
                    "source_file": page["source_file"],
                    "page_number": page["page_number"],
                    "text": chunk_text,
                }
            )
            chunk_id += 1

    return all_chunks


def main():
    json_files = list(PROCESSED_DIR.glob("*.json"))

    for json_path in tqdm(json_files, desc="Chunking files"):
        chunked_data = process_file(json_path)
        output_path = CHUNKS_DIR / f"{json_path.stem}_chunks.json"
        save_json(chunked_data, output_path)


if __name__ == "__main__":
    main()