import re
from pathlib import Path
from tqdm import tqdm

from utils.config import PROCESSED_DIR
from utils.file_io import load_json, save_json


def clean_text(text: str) -> str:
    # remove excessive newlines
    text = re.sub(r"\n+", "\n", text)

    # replace newlines with space (for better semantic flow)
    text = text.replace("\n", " ")

    # remove multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def process_file(json_path: Path):
    data = load_json(json_path)

    cleaned = []
    for item in data:
        cleaned.append(
            {
                "source_file": item["source_file"],
                "page_number": item["page_number"],
                "text": clean_text(item["text"]),
            }
        )

    return cleaned


def main():
    json_files = list(PROCESSED_DIR.glob("*.json"))

    for json_path in tqdm(json_files, desc="Cleaning text"):
        cleaned_data = process_file(json_path)

        output_path = json_path  # overwrite same file
        save_json(cleaned_data, output_path)


if __name__ == "__main__":
    main()