from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path
from uuid import uuid4
import cv2
import asyncio

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserRead
from app.services.face_embedding_model import get_embedding, save_embedding
from app.services.image_storage import save_user_image

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserRead)
async def register_user(
    name: str = Form(..., description="Full name"),
    employee_id: str = Form(..., description="Unique employee ID"),
    image: UploadFile = File(..., description="Face photo (JPG/PNG)"),
    db: AsyncSession = Depends(get_db),
):
    """Register new employee with face embedding."""
    if not image.content_type.startswith("image/"):
        raise HTTPException(400, "Only image files allowed")

    # 1. Save image
    image_path = await save_user_image(image, employee_id)

    # 2. Generate embedding
    img_bgr = await asyncio.to_thread(cv2.imread, image_path)
    if img_bgr is None:
        raise HTTPException(400, "Invalid image file")

    embedding = get_embedding(img_bgr)
    if embedding is None:
        raise HTTPException(422, "No face detected! Please upload clear frontal face photo")

    # 3. Save embedding
    emb_dir = Path(settings.embedding_dir)
    emb_dir.mkdir(parents=True, exist_ok=True)
    emb_filename = f"{employee_id}_{uuid4().hex}.npy"
    emb_path = str(emb_dir / emb_filename)
    save_embedding(embedding, emb_path)

    # 4. Create user
    user = User(
        name=name,
        employee_id=employee_id,
        image_path=image_path,
        embedding_path=emb_path,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user