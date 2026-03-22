from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from utils.config import CHUNKS_DIR, INDEX_DIR


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    all_chunks = []

    chunk_files = list(CHUNKS_DIR.glob("*_chunks.json"))
    for chunk_file in chunk_files:
        with open(chunk_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_chunks.extend(data)

    return all_chunks


def main():
    print("Loading chunk files...")
    chunks = load_chunks()

    if not chunks:
        print("No chunks found.")
        return

    print(f"Loaded {len(chunks)} chunks")

    texts = [item["text"] for item in chunks]

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    embeddings = np.array(embeddings).astype("float32")
    dimension = embeddings.shape[1]

    print(f"Embedding shape: {embeddings.shape}")

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(index, str(INDEX_DIR / "faiss_index.bin"))

    with open(INDEX_DIR / "chunks_metadata.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Saved FAISS index to: {INDEX_DIR / 'faiss_index.bin'}")
    print(f"Saved metadata to: {INDEX_DIR / 'chunks_metadata.json'}")


if __name__ == "__main__":
    main()