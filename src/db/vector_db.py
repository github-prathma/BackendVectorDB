from typing import List, Dict, Any, Optional
import numpy as np
import threading

class BruteForceIndex:
    def __init__(self):
        self.vectors: List[np.ndarray] = []
        self.ids: List[str] = []
        self.lock = threading.Lock()

    def add(self, doc_id: str, vector: np.ndarray):
        with self.lock:
            self.ids.append(doc_id)
            self.vectors.append(vector)

    def remove(self, doc_id: str):
        with self.lock:
            if doc_id in self.ids:
                idx = self.ids.index(doc_id)
                self.ids.pop(idx)
                self.vectors.pop(idx)

    def query(self, vector: np.ndarray, top_k: int = 5) -> List[str]:
        with self.lock:
            if not self.vectors:
                return []
            distances = [np.linalg.norm(v - vector) for v in self.vectors]
            nearest = np.argsort(distances)[:top_k]
            return [self.ids[i] for i in nearest]

class BallTreeNode:
    def __init__(self, indices, vectors, ids, leaf_size=10):
        self.indices = indices
        self.left = None
        self.right = None
        self.center = np.mean(vectors[indices], axis=0)
        self.radius = np.max([np.linalg.norm(vectors[i] - self.center) for i in indices])
        self.ids = [ids[i] for i in indices]
        self.is_leaf = len(indices) <= leaf_size
        if not self.is_leaf:
            # Pick two farthest points as pivots
            dists = np.array([[np.linalg.norm(vectors[i] - vectors[j]) for j in indices] for i in indices])
            i1, i2 = np.unravel_index(np.argmax(dists), dists.shape)
            pivot1 = indices[i1]
            pivot2 = indices[i2]
            left_indices = [i for i in indices if np.linalg.norm(vectors[i] - vectors[pivot1]) < np.linalg.norm(vectors[i] - vectors[pivot2])]
            right_indices = [i for i in indices if i not in left_indices]
            self.left = BallTreeNode(left_indices, vectors, ids, leaf_size)
            self.right = BallTreeNode(right_indices, vectors, ids, leaf_size)

    def knn(self, vector, top_k, heap):
        import heapq
        if self.is_leaf:
            for idx in self.indices:
                dist = np.linalg.norm(vector - self.center)
                heapq.heappush(heap, (dist, self.ids[self.indices.index(idx)]))
        else:
            # Visit closer child first
            d_left = np.linalg.norm(vector - self.left.center) if self.left else float('inf')
            d_right = np.linalg.norm(vector - self.right.center) if self.right else float('inf')
            children = [(d_left, self.left), (d_right, self.right)]
            children.sort()
            for _, child in children:
                if child:
                    child.knn(vector, top_k, heap)

class BallTreeIndex:
    def __init__(self, leaf_size=10):
        self.vectors: List[np.ndarray] = []
        self.ids: List[str] = []
        self.leaf_size = leaf_size
        self.root: Optional[BallTreeNode] = None
        self.lock = threading.Lock()

    def add(self, doc_id: str, vector: np.ndarray):
        with self.lock:
            self.ids.append(doc_id)
            self.vectors.append(vector)
            self.root = None  # Invalidate tree

    def remove(self, doc_id: str):
        with self.lock:
            if doc_id in self.ids:
                idx = self.ids.index(doc_id)
                self.ids.pop(idx)
                self.vectors.pop(idx)
                self.root = None

    def build(self):
        with self.lock:
            if self.vectors:
                self.root = BallTreeNode(list(range(len(self.vectors))), self.vectors, self.ids, self.leaf_size)

    def query(self, vector: np.ndarray, top_k: int = 5) -> List[str]:
        with self.lock:
            if not self.vectors:
                return []
            if self.root is None:
                self.build()
            import heapq
            heap = []
            self.root.knn(vector, top_k, heap)
            heap.sort()
            return [doc_id for _, doc_id in heap[:top_k]]

class VectorDB:
    def __init__(self, index_type: str = 'brute'):
        self.index_type = index_type
        if index_type == 'brute':
            self.index = BruteForceIndex()
        elif index_type == 'balltree':
            self.index = BallTreeIndex()
        else:
            raise ValueError('Unknown index type')
        self.vector_map: Dict[str, np.ndarray] = {}
        self.lock = threading.Lock()

    def index_document(self, doc_id: str, vector: np.ndarray) -> None:
        with self.lock:
            if doc_id in self.vector_map:
                raise ValueError("Document ID already exists.")
            self.vector_map[doc_id] = vector
            self.index.add(doc_id, vector)

    def query(self, vector: np.ndarray, top_k: int = 5) -> List[str]:
        with self.lock:
            return self.index.query(vector, top_k)

    def delete_document(self, doc_id: str) -> None:
        with self.lock:
            if doc_id not in self.vector_map:
                raise ValueError("Document ID does not exist.")
            del self.vector_map[doc_id]
            self.index.remove(doc_id)