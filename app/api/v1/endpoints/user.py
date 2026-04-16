from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["Users"])

UPLOAD_DIR = Path("uploads/users")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/register", response_model=UserRead)
async def register_user(
    name: str = Form(...),
    employee_id: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    ext = Path(image.filename).suffix
    filename = f"{uuid4().hex}{ext}"
    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    user = User(
        name=name,
        employee_id=employee_id,
        image_path=str(file_path),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user