"""
Production face matching with cosine similarity.
Threshold: 0.68 (DeepFace ArcFace standard).
"""
import numpy as np
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.services.face_embedding_model import get_embedding, load_embedding

SIMILARITY_THRESHOLD = 0.68  # ArcFace standard [web:59]

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 512-dim embeddings."""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

async def find_matched_user_id(frame_bgr: np.ndarray, db: AsyncSession) -> tuple[int | None, float]:
    """
    Returns (user_id, confidence_score) or (None, 0.0).
    Confidence: 0.0-1.0 cosine similarity.
    """
    live_embedding = get_embedding(frame_bgr)
    if live_embedding is None:
        return None, 0.0

    # Get all users with embeddings
    result = await db.execute(select(User).where(User.embedding_path.isnot(None)))
    users = result.scalars().all()

    best_score = 0.0
    best_user_id = None

    for user in users:
        try:
            stored_embedding = await asyncio.to_thread(np.load, user.embedding_path)
            score = cosine_similarity(live_embedding, stored_embedding)
            if score > best_score:
                best_score = score
                best_user_id = user.id
        except Exception as e:
            print(f"⚠️ Failed to load embedding {user.embedding_path}: {e}")
            continue

    return (best_user_id, best_score) if best_score >= SIMILARITY_THRESHOLD else (None, best_score)