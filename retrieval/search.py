import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from utils.config import INDEX_DIR


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_index_and_metadata():
    index = faiss.read_index(str(INDEX_DIR / "faiss_index.bin"))

    with open(INDEX_DIR / "chunks_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata


def search(query: str, top_k: int = 5):
    print("Loading model...")
    model = SentenceTransformer(MODEL_NAME)

    print("Loading FAISS index and metadata...")
    index, metadata = load_index_and_metadata()

    print("Embedding query...")
    query_embedding = model.encode([query], convert_to_numpy=True).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        item = metadata[idx]
        results.append(
            {
                "rank": rank + 1,
                "distance": float(distances[0][rank]),
                "chunk_id": item["chunk_id"],
                "source_file": item["source_file"],
                "page_number": item["page_number"],
                "text": item["text"],
            }
        )

    return results


def main():
    query = input("Enter your search query: ").strip()

    if not query:
        print("Query cannot be empty.")
        return

    results = search(query, top_k=5)

    print("\nTop results:\n")
    for r in results:
        print("=" * 80)
        print(f"Rank: {r['rank']}")
        print(f"Distance: {r['distance']:.4f}")
        print(f"Chunk ID: {r['chunk_id']}")
        print(f"Source: {r['source_file']} | Page: {r['page_number']}")
        print(f"Text: {r['text']}")
        print()


if __name__ == "__main__":
    main()