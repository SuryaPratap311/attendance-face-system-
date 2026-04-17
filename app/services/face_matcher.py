from pathlib import Path
from typing import Optional, List

import numpy as np
from sklearn.neighbors import NearestNeighbors


def load_all_embeddings(embedding_dir: str) -> (List[str], np.ndarray):
    emb_dir = Path(embedding_dir)
    employee_ids = []
    embeddings = []

    if not emb_dir.exists():
        return [], np.array([])

    for p in emb_dir.iterdir():
        if p.suffix != ".npy":
            continue
        try:
            emp_id = p.name.split("_")[0]
            emb = np.load(str(p)).squeeze()
            employee_ids.append(emp_id)
            embeddings.append(emb)
        except Exception:
            continue

    if not embeddings:
        return [], np.array([])

    return employee_ids, np.array(embeddings)


class FaceMatcher:
    def __init__(self, embedding_dir: str):
        self.embedding_dir = embedding_dir

    def match_face(self, query_embedding: np.ndarray, threshold: float = 0.30) -> Optional[str]:
        employee_ids, embeddings = load_all_embeddings(self.embedding_dir)

        if len(employee_ids) == 0:
            return None

        ann = NearestNeighbors(n_neighbors=1, metric="cosine").fit(embeddings)
        q = query_embedding.reshape(1, -1)
        dist, idx = ann.kneighbors(q)
        min_dist = float(dist[0, 0])

        if min_dist > threshold:
            return None

        return employee_ids[int(idx[0, 0])]


def get_face_matcher():
    from app.core.config import settings
    return FaceMatcher(settings.embedding_dir)