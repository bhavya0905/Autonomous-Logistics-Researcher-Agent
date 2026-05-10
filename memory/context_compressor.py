from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class ContextCompressor:

    def __init__(
        self,
        max_chunks: int = 8,
        similarity_threshold: float = 0.85,
        lambda_param: float = 0.7,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    ):
        self.max_chunks = max_chunks
        self.similarity_threshold = similarity_threshold
        self.lambda_param = lambda_param
        self.embedder = SentenceTransformer(model_name)

    def _embed(self, texts: List[str]):
        return self.embedder.encode(texts)

    def _remove_duplicates(self, docs: List[Dict], embeddings):

        unique_docs = []
        unique_embeddings = []

        for i, doc in enumerate(docs):

            emb = embeddings[i]
            duplicate = False

            for prev_emb in unique_embeddings:
                sim = cosine_similarity([emb], [prev_emb])[0][0]

                if sim > self.similarity_threshold:
                    duplicate = True
                    break

            if not duplicate:
                unique_docs.append(doc)
                unique_embeddings.append(emb)

        return unique_docs, np.array(unique_embeddings)

    def _mmr(self, query_emb, doc_embs, docs):

        selected = []
        selected_indices = []

        sim_query = cosine_similarity([query_emb], doc_embs)[0]

        while len(selected) < min(self.max_chunks, len(docs)):

            if len(selected) == 0:
                idx = np.argmax(sim_query)
                selected.append(docs[idx])
                selected_indices.append(idx)
                continue

            mmr_scores = []

            for i in range(len(docs)):

                if i in selected_indices:
                    mmr_scores.append(-1)
                    continue

                relevance = sim_query[i]

                diversity = max(
                    cosine_similarity(
                        [doc_embs[i]],
                        [doc_embs[j]]
                    )[0][0]
                    for j in selected_indices
                )

                score = (
                    self.lambda_param * relevance
                    - (1 - self.lambda_param) * diversity
                )

                mmr_scores.append(score)

            idx = np.argmax(mmr_scores)

            selected.append(docs[idx])
            selected_indices.append(idx)

        return selected

    def compress(self, query: str, docs: List[Dict]) -> List[Dict]:

        if not docs:
            return []

        texts = [d["text"] for d in docs]

        doc_embeddings = self._embed(texts)
        query_embedding = self._embed([query])[0]

        docs, doc_embeddings = self._remove_duplicates(
            docs,
            doc_embeddings
        )

        compressed_docs = self._mmr(
            query_embedding,
            doc_embeddings,
            docs
        )

        return compressed_docs