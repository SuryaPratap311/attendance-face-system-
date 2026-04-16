from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.user import UserCreate, UserRead
from app.schemas.attendance import AttendanceRead
from app.services.attendance_service import mark_attendance

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/mark/{user_id}", response_model=AttendanceRead)
async def mark_user_attendance(user_id: int, db: AsyncSession = Depends(get_db)):
    return await mark_attendance(db, user_id=user_id)