# app/api/v1/endpoints/attendance.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.camera_service import capture_frame_from_camera
from app.services.face_embedding_model import get_embedding
from app.services.face_matcher import get_face_matcher
from app.services.attendance_service import mark_attendance

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/mark")
async def mark_attendance_endpoint(db: AsyncSession = Depends(get_db)):
    frame_bgr = capture_frame_from_camera()
    if frame_bgr is None:
        raise HTTPException(status_code=500, detail="Camera capture failed")

    embedding = get_embedding(frame_bgr)
    if embedding is None:
        raise HTTPException(status_code=422, detail="No face detected")

    matcher = get_face_matcher()
    emp_id = matcher.match_face(embedding, threshold=0.35)

    if emp_id is None:
        raise HTTPException(status_code=404, detail="Face not found")

    attendance = await mark_attendance(db, employee_id=emp_id)

    return {
        "message": "Attendance marked successfully",
        "employee_id": emp_id,
        "status": attendance.status,
        "timestamp": attendance.timestamp,
    }