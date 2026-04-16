"""
Production-grade face embedding using DeepFace (ArcFace).
512-dim embeddings, no compilation issues.
"""
import cv2
import numpy as np
from deepface import DeepFace
from pathlib import Path

def get_embedding(image_bgr: np.ndarray) -> np.ndarray | None:
    """Extract 512-dim ArcFace embedding from BGR image."""
    try:
        rgb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result = DeepFace.represent(
            rgb_image, 
            model_name="ArcFace",  # Best accuracy
            enforce_detection=False,
            detector_backend="opencv",
            silent=True
        )
        return np.array(result[0]["embedding"])
    except Exception:
        return None

def save_embedding(embedding: np.ndarray, path: str):
    """Save embedding as .npy file."""
    np.save(path, embedding)

def load_embedding(path: str) -> np.ndarray:
    """Load embedding from .npy file."""
    return np.load(path)