from ultralytics import YOLO
from app.core.config import settings

_model = None

def get_model():
    global _model
    if _model is None:
        print(f"Loading YOLO model: {settings.yolo_model_path}")
        _model = YOLO(settings.yolo_model_path)
    return _model

def detect(frame):
    return get_model().predict(source=frame, verbose=False)