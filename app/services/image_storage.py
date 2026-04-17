from pathlib import Path
from uuid import uuid4
import cv2
from app.core.config import settings

def save_captured_image(frame_bgr, employee_id: str) -> str:
    upload_dir = Path(settings.image_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{employee_id}_{uuid4().hex}.jpg"
    file_path = upload_dir / filename

    cv2.imwrite(str(file_path), frame_bgr)
    return str(file_path)

def save_user_image(image, employee_id: str) -> str:
    return save_captured_image(image, employee_id)