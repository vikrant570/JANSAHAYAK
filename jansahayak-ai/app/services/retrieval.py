import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMES_FILE = BASE_DIR / "data" / "schemes.json"


class SchemeRetriever:

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.schemes = self.load_schemes()

        self.documents = [
            self.scheme_to_text(scheme)
            for scheme in self.schemes
        ]

        self.index = None

        if not self.documents:
            return

        embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

    def load_schemes(self) -> list[dict]:

        if not SCHEMES_FILE.exists():
            return []

        try:
            with open(
                SCHEMES_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                schemes = json.load(file)

        except Exception as error:

            print(
                f"Error loading schemes.json: {error}"
            )

            return []

        # Only use verified schemes
        verified_schemes = []

        for scheme in schemes:

            if scheme.get(
                "verification_status"
            ) == "verified":

                verified_schemes.append(
                    scheme
                )

        return verified_schemes

    def scheme_to_text(
        self,
        scheme: dict
    ) -> str:

        eligibility = scheme.get(
            "eligibility",
            {}
        )

        return " ".join([

            scheme.get(
                "name",
                ""
            ),

            scheme.get(
                "category",
                ""
            ),

            scheme.get(
                "description",
                ""
            ),

            " ".join(
                scheme.get(
                    "target_users",
                    []
                )
            ),

            " ".join(
                scheme.get(
                    "states",
                    []
                )
            ),

            " ".join(
                scheme.get(
                    "benefits",
                    []
                )
            ),

            " ".join(
                scheme.get(
                    "documents",
                    []
                )
            ),

            " ".join(
                eligibility.get(
                    "occupation",
                    []
                )
            ),

            " ".join(
                eligibility.get(
                    "education",
                    []
                )
            ),

            " ".join(
                eligibility.get(
                    "other_conditions",
                    []
                )
            )
        ])

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[dict]:

        if (
            self.index is None
            or not self.schemes
        ):
            return []

        query_embedding = (
            self.model.encode(
                [query],
                convert_to_numpy=True,
                normalize_embeddings=True
            )
            .astype("float32")
        )

        scores, indices = self.index.search(
            query_embedding,
            min(
                top_k,
                len(self.schemes)
            )
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue

            scheme = dict(
                self.schemes[index]
            )

            scheme[
                "retrieval_score"
            ] = round(
                float(score),
                4
            )

            results.append(
                scheme
            )

        return results


# -------------------------------------------------
# BACKWARD COMPATIBILITY
# -------------------------------------------------
# Your existing analyzer.py expects:
#
# from app.services.retrieval import search_schemes
#
# So we keep this function.
# -------------------------------------------------

_retriever = None


def search_schemes(
    query: str,
    top_k: int = 5
) -> list[dict]:

    global _retriever

    if _retriever is None:

        _retriever = SchemeRetriever()

    return _retriever.search(
        query=query,
        top_k=top_k
    )
# -----------------------------------------
# BACKWARD COMPATIBILITY
# -----------------------------------------

def load_schemes() -> list[dict]:
    """
    Backward-compatible helper used by
    routes_schemes.py.
    """

    if not SCHEMES_FILE.exists():
        return []

    with open(
        SCHEMES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        schemes = json.load(file)

    return schemes