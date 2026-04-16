from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads/users")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def save_user_image(image: UploadFile, user_name: str) -> str:
    ext = Path(image.filename).suffix
    filename = f"{user_name}_{uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / filename

    content = await image.read()
    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)