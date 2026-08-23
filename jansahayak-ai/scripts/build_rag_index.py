import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


SCHEMES_FILE = Path("data/schemes.json")
RAG_DIR = Path("data/rag")

INDEX_FILE = RAG_DIR / "scheme_index.faiss"
METADATA_FILE = RAG_DIR / "scheme_metadata.json"


def build_search_text(scheme):
    eligibility = scheme.get("eligibility", {})

    return f"""
Scheme name: {scheme.get("name", "")}

Category: {scheme.get("category", "")}

Description: {scheme.get("description", "")}

Target users: {", ".join(scheme.get("target_users", []))}

States: {", ".join(scheme.get("states", []))}

Benefits: {", ".join(scheme.get("benefits", []))}

Occupation eligibility: {", ".join(
    eligibility.get("occupation", [])
)}

Education eligibility: {", ".join(
    eligibility.get("education", [])
)}

Other eligibility conditions: {", ".join(
    eligibility.get("other_conditions", [])
)}

Required documents: {", ".join(
    scheme.get("documents", [])
)}

Application steps: {", ".join(
    scheme.get("application_steps", [])
)}

Ministry: {scheme.get("nodal_ministry", "")}

Level: {scheme.get("level", "")}

Tags: {", ".join(scheme.get("tags", []))}
""".strip()


def main():

    print("=" * 70)
    print("JANSAHAYAK - BUILD REAL RAG INDEX")
    print("=" * 70)

    with open(
        SCHEMES_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        schemes = json.load(file)

    print(f"\nSchemes loaded: {len(schemes)}")

    # Safety check
    schemes = [
        s for s in schemes
        if s.get("name")
        and s["name"].strip().lower() != "example scheme"
    ]

    print(
        f"Schemes after safety filter: "
        f"{len(schemes)}"
    )

    search_texts = [
        build_search_text(scheme)
        for scheme in schemes
    ]

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Generating embeddings...")

    embeddings = model.encode(
        search_texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    RAG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    metadata = []

    for scheme, text in zip(
        schemes,
        search_texts
    ):

        metadata.append({
            **scheme,
            "search_text": text
        })

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n" + "=" * 70)
    print("RAG INDEX BUILT SUCCESSFULLY")
    print("=" * 70)

    print("Index:", INDEX_FILE)
    print("Metadata:", METADATA_FILE)
    print("Vectors:", index.ntotal)
    print("Dimension:", dimension)

    print("\nFirst 5 indexed schemes:")

    for i, scheme in enumerate(
        schemes[:5],
        start=1
    ):
        print(
            f"{i}. {scheme['name']}"
        )


if __name__ == "__main__":
    main()