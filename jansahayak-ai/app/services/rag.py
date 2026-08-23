import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMES_FILE = BASE_DIR / "data" / "schemes.json"


class SchemeRAG:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(model_name)

        self.schemes = self._load_schemes()

        self.documents = self._create_documents()

        self.embeddings = self.model.encode(
            self.documents,
            convert_to_numpy=True
        ).astype("float32")

        dimension = self.embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(self.embeddings)

    def _load_schemes(self):

        with open(
            SCHEMES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    def _create_documents(self):

        documents = []

        for scheme in self.schemes:

            eligibility = scheme.get(
                "eligibility",
                {}
            )

            text = f"""
            Scheme name:
            {scheme.get("name", "")}

            Category:
            {scheme.get("category", "")}

            Description:
            {scheme.get("description", "")}

            Target users:
            {", ".join(scheme.get("target_users", []))}

            States:
            {", ".join(scheme.get("states", []))}

            Occupations:
            {", ".join(
                eligibility.get("occupation", [])
            )}

            Education:
            {", ".join(
                eligibility.get("education", [])
            )}

            Other conditions:
            {", ".join(
                eligibility.get("other_conditions", [])
            )}

            Benefits:
            {", ".join(scheme.get("benefits", []))}

            Documents:
            {", ".join(scheme.get("documents", []))}
            """

            documents.append(text)

        return documents

    def search(
        self,
        query: str,
        top_k: int = 3
    ):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index < 0:
                continue

            scheme = self.schemes[index].copy()

            scheme["_retrieval_distance"] = float(
                distance
            )

            results.append(scheme)

        return results


_rag_instance = None


def get_rag():

    global _rag_instance

    if _rag_instance is None:
        _rag_instance = SchemeRAG()

    return _rag_instance