from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import cv2
import asyncio
import numpy as np

from app.core.database import get_db
from app.schemas.attendance import AttendanceRead
from app.services.attendance_service import mark_attendance
from app.services.face_matcher import find_matched_user_id
from app.services.image_storage import save_user_image

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/scan", response_model=AttendanceRead)
async def scan_face_and_mark(
    image: UploadFile = File(..., description="Face photo for attendance"),
    db: AsyncSession = Depends(get_db),
):
    """User apna face photo upload kare — auto match karke attendance mark ho jaegi."""

    if not image.content_type.startswith("image/"):
        raise HTTPException(400, "Sirf image files allowed hain")

    # 1. Image bytes read karo aur OpenCV frame banao
    contents = await image.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame_bgr = await asyncio.to_thread(cv2.imdecode, np_arr, cv2.IMREAD_COLOR)

    if frame_bgr is None:
        raise HTTPException(400, "Invalid image — decode nahi hua")

    # 2. Face match karo DB ke saare users se
    user_id, confidence = await find_matched_user_id(frame_bgr, db)

    if user_id is None:
        raise HTTPException(
            404,
            f"Match Not Found (best score: {confidence:.2f}). "
            "Clear frontal face photo upload karein."
        )

    # 3. Attendance mark karo
    attendance = await mark_attendance(db, user_id=user_id)
    return attendance