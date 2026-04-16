"""
Production-grade face embedding using DeepFace (ArcFace).
512-dim embeddings, no compilation issues.
"""
import cv2
import numpy as np
from deepface import DeepFace
from pathlib import Path
from app.core.config import settings

def get_embedding(image_bgr: np.ndarray) -> np.ndarray | None:
    """Extract 512-dim ArcFace embedding from BGR image."""
    try:
        rgb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result = DeepFace.represent(
            rgb_image, 
            model_name="ArcFace",
            enforce_detection=True,  
            detector_backend="opencv",
            silent=True
        )
        embedding = np.array(result[0]["embedding"])
        return embedding.astype(np.float32)  # ← Consistent dtype
    except Exception as e:
        print(f"Embedding failed: {e}")  # ← Debug info
        return None
    
def save_embedding(embedding: np.ndarray, path: str):
    """Save embedding as .npy file."""
    np.save(path, embedding)

def load_embedding(path: str) -> np.ndarray:
    """Load embedding from .npy file."""
    return np.load(path)