import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


class SchemeRAG:

    def __init__(self):

        self.index_path = Path(
            "data/rag/scheme_index.faiss"
        )

        self.metadata_path = Path(
            "data/rag/scheme_metadata.json"
        )

        self.index = faiss.read_index(
            str(self.index_path)
        )

        with open(
            self.metadata_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.metadata = json.load(file)

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        scores, indices = self.index.search(
            embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            scheme = self.metadata[index].copy()

            scheme["retrieval_score"] = float(
                score
            )

            results.append(
                scheme
            )

        return results