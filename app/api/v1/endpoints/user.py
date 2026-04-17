from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pathlib import Path
from uuid import uuid4

from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.services.camera_service import capture_frame_from_camera
from app.services.image_storage import save_captured_image
from app.services.face_embedding_model import get_embedding, save_embedding
from app.services.face_matcher import FaceMatcher


router = APIRouter(prefix="/users", tags=["Users"])


# Global FaceMatcher (lazily initialized)
_face_matcher: FaceMatcher | None = None


def get_face_matcher() -> FaceMatcher:
    global _face_matcher
    if _face_matcher is None:
        _face_matcher = FaceMatcher(embedding_dir=settings.embedding_dir)
    return _face_matcher


async def generate_employee_id(db: AsyncSession) -> str:
    result = await db.execute(select(User.employee_id))
    ids = result.scalars().all()

    max_num = 0
    for emp_id in ids:
        try:
            num = int(emp_id.replace("EMP", ""))
            if num > max_num:
                max_num = num
        except Exception:
            continue

    return f"EMP{max_num + 1:03d}"


@router.post("/register", response_model=UserRead, status_code=201)
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    employee_id = await generate_employee_id(db)

    user = User(
        employee_id=employee_id,
        name=payload.name,
        role=payload.role,
        department=payload.department,
        status="pending_photo",
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/capture-photo/{employee_id}", response_model=UserRead)
async def capture_photo(employee_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.employee_id == employee_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="Employee not found")

    if user.status == "registered":
        raise HTTPException(
            status_code=409,
            detail="Photo already captured for this employee"
        )

    frame_bgr = capture_frame_from_camera()
    if frame_bgr is None:
        raise HTTPException(status_code=500, detail="Camera capture failed")

    embedding = get_embedding(frame_bgr)
    if embedding is None:
        raise HTTPException(status_code=422, detail="No face detected")

    image_path = save_captured_image(frame_bgr, employee_id)

    emb_dir = Path(settings.embedding_dir)
    emb_dir.mkdir(parents=True, exist_ok=True)
    embedding_path = str(emb_dir / f"{employee_id}_{uuid4().hex}.npy")
    save_embedding(embedding, embedding_path)

    user.image_path = image_path
    user.embedding_path = embedding_path
    user.status = "registered"

    await db.commit()
    await db.refresh(user)
    return user