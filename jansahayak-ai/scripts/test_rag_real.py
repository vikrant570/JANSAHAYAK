import json

import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = "data/rag/scheme_index.faiss"
METADATA_FILE = "data/rag/scheme_metadata.json"


def search(query, top_k=5):

    index = faiss.read_index(
        INDEX_FILE
    )

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(
        embedding,
        top_k
    )

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    for rank, (score, idx) in enumerate(
        zip(scores[0], indices[0]),
        start=1
    ):

        if idx == -1:
            continue

        scheme = metadata[idx]

        print(
            f"\n{rank}. {scheme['name']}"
        )

        print(
            f"Category: {scheme.get('category')}"
        )

        print(
            f"State: {scheme.get('states')}"
        )

        print(
            f"Score: {round(float(score), 4)}"
        )

        print(
            f"Source: {scheme.get('official_source')}"
        )


def main():

    queries = [
        "I am a farmer and need financial assistance",
        "I am a student looking for scholarship",
        "I want government support for business",
        "I need health insurance assistance",
    ]

    for query in queries:
        search(query)


if __name__ == "__main__":
    main()