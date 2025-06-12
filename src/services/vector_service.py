import numpy as np
from src.db.vector_db import VectorDB

class VectorService:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

    def index_chunks(self, chunk_ids, embeddings):
        if len(chunk_ids) != len(embeddings):
            raise ValueError("Embeddings count mismatch")
        for chunk_id, emb in zip(chunk_ids, embeddings):
            self.vector_db.index_document(chunk_id, np.array(emb))

    def search(self, query_embedding, top_k=5):
        return self.vector_db.query(np.array(query_embedding), top_k=top_k)
