from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile
from app.core.config import settings  

async def save_user_image(image: UploadFile, employee_id: str) -> str: 
    """Save uploaded user image with employee_id."""
    upload_dir = Path(settings.image_dir) 
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    ext = Path(image.filename).suffix
    filename = f"{employee_id}_{uuid4().hex}{ext}"
    file_path = upload_dir / filename

    content = await image.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)