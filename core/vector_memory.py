# core/vector_memory.py
import faiss
import numpy as np

class VectorMemory:
    """
    Semantic memory using FAISS for embedding storage.
    """
    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

    def add(self, vector, meta):
        """
        Add a vector with associated metadata.
        """
        self.index.add(np.array([vector]).astype('float32'))
        self.metadata.append(meta)

    def search(self, query_vector, k=5):
        """
        Return top-k metadata for nearest neighbors to query_vector.
        """
        D, I = self.index.search(np.array([query_vector]).astype('float32'), k)
        results = []
        for distances, indices in zip(D, I):
            for dist, idx in zip(distances, indices):
                results.append((self.metadata[idx], dist))
        return results
