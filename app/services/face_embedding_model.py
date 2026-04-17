import cv2
import numpy as np
from deepface import DeepFace

def get_embedding(image_bgr: np.ndarray) -> np.ndarray | None:
    try:
        rgb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result = DeepFace.represent(
            rgb_image,
            model_name="ArcFace",
            enforce_detection=True,
            detector_backend="opencv"
        )
        embedding = np.array(result[0]["embedding"])
        return embedding.astype(np.float32)
    except Exception as e:
        print(f"Embedding failed: {e}")
        return None

def save_embedding(embedding: np.ndarray, path: str) -> str:
    np.save(path, embedding)
    return path

def load_embedding(path: str) -> np.ndarray:
    return np.load(path)