from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import settings  

async def save_user_image(image: UploadFile, employee_id: str) -> str: 
    """Save uploaded user image with employee_id."""
    UPLOAD_DIR = settings.image_dir  # ← Use config
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    ext = Path(image.filename).suffix
    filename = f"{employee_id}_{uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / filename

    content = await image.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)