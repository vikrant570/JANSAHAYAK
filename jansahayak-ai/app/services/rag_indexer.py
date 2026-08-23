import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]

SCHEMES_FILE = BASE_DIR / "data" / "schemes.json"

RAG_DIR = BASE_DIR / "data" / "rag"

INDEX_FILE = RAG_DIR / "scheme_index.faiss"

METADATA_FILE = RAG_DIR / "scheme_metadata.json"


class SchemeRAGIndexer:

    def __init__(self):

        RAG_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            "Loading embedding model..."
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print(
            "Embedding model loaded."
        )

    # -----------------------------------------
    # LOAD SCHEMES
    # -----------------------------------------

    def load_schemes(self):

        if not SCHEMES_FILE.exists():

            raise FileNotFoundError(
                f"Schemes file not found: "
                f"{SCHEMES_FILE}"
            )

        with open(
            SCHEMES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):

            # Supports:
            # {"schemes": [...]}

            schemes = data.get(
                "schemes",
                []
            )

        elif isinstance(data, list):

            schemes = data

        else:

            raise ValueError(
                "Invalid schemes.json format"
            )

        return schemes

    # -----------------------------------------
    # CREATE SEARCH TEXT
    # -----------------------------------------

    def scheme_to_text(
        self,
        scheme: dict
    ) -> str:

        eligibility = scheme.get(
            "eligibility",
            {}
        )

        text_parts = [

            f"Scheme name: "
            f"{scheme.get('name', '')}",

            f"Category: "
            f"{scheme.get('category', '')}",

            f"Description: "
            f"{scheme.get('description', '')}",

            "Target users: "
            + ", ".join(
                scheme.get(
                    "target_users",
                    []
                )
            ),

            "States: "
            + ", ".join(
                scheme.get(
                    "states",
                    []
                )
            ),

            "Benefits: "
            + ", ".join(
                scheme.get(
                    "benefits",
                    []
                )
            ),

            "Occupation eligibility: "
            + ", ".join(
                eligibility.get(
                    "occupation",
                    []
                )
            ),

            "Education eligibility: "
            + ", ".join(
                eligibility.get(
                    "education",
                    []
                )
            ),

            "Other eligibility conditions: "
            + ", ".join(
                eligibility.get(
                    "other_conditions",
                    []
                )
            ),

            "Required documents: "
            + ", ".join(
                scheme.get(
                    "documents",
                    []
                )
            ),

            "Application steps: "
            + " ".join(
                scheme.get(
                    "application_steps",
                    []
                )
            )
        ]

        return "\n".join(
            part
            for part in text_parts
            if part.strip()
        )

    # -----------------------------------------
    # BUILD INDEX
    # -----------------------------------------

    def build(self):

        schemes = self.load_schemes()

        if not schemes:

            raise ValueError(
                "No schemes found."
            )

        documents = []

        metadata = []

        for scheme in schemes:

            text = self.scheme_to_text(
                scheme
            )

            documents.append(text)

            metadata.append({

                "id": scheme.get(
                    "id",
                    ""
                ),

                "name": scheme.get(
                    "name",
                    ""
                ),

                "category": scheme.get(
                    "category",
                    ""
                ),

                "description": scheme.get(
                    "description",
                    ""
                ),

                "target_users": scheme.get(
                    "target_users",
                    []
                ),

                "states": scheme.get(
                    "states",
                    []
                ),

                "eligibility": scheme.get(
                    "eligibility",
                    {}
                ),

                "benefits": scheme.get(
                    "benefits",
                    []
                ),

                "documents": scheme.get(
                    "documents",
                    []
                ),

                "application_steps": scheme.get(
                    "application_steps",
                    []
                ),

                "official_source": scheme.get(
                    "official_source",
                    ""
                ),

                "source_name": scheme.get(
                    "source_name",
                    ""
                ),

                "last_verified": scheme.get(
                    "last_verified",
                    ""
                ),

                "verification_status":
                    scheme.get(
                        "verification_status",
                        "unknown"
                    ),

                "search_text": text

            })

        print(
            f"Creating embeddings for "
            f"{len(documents)} schemes..."
        )

        embeddings = self.model.encode(
            documents,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        embeddings = embeddings.astype(
            "float32"
        )

        # Normalize vectors for cosine similarity
        faiss.normalize_L2(
            embeddings
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(
            embeddings
        )

        faiss.write_index(
            index,
            str(INDEX_FILE)
        )

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

        print()
        print(
            "================================"
        )
        print(
            "RAG INDEX CREATED SUCCESSFULLY"
        )
        print(
            "================================"
        )

        print(
            f"Schemes indexed: "
            f"{len(documents)}"
        )

        print(
            f"Vector dimension: "
            f"{dimension}"
        )

        print(
            f"Index: {INDEX_FILE}"
        )

        print(
            f"Metadata: {METADATA_FILE}"
        )


if __name__ == "__main__":

    indexer = SchemeRAGIndexer()

    indexer.build()