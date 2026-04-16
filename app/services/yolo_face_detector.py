from ultralytics import YOLO
from app.core.config import settings

model = YOLO(settings.yolo_model_path)

def detect(frame):
    return model.predict(source=frame, verbose=False)