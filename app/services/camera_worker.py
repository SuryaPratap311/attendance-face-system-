"""
Production live camera with auto attendance marking.
"""
import cv2
import asyncio
from datetime import datetime
from app.services.face_matcher import find_matched_user_id
from app.services.attendance_service import mark_attendance
from app.core.database import AsyncSessionLocal

async def process_frame_and_mark(frame_bgr):
    """Process single frame, return user_id if matched."""
    async with AsyncSessionLocal() as db:
        user_id, confidence = await find_matched_user_id(frame_bgr, db)
        if user_id:
            await mark_attendance(db, user_id)
            print(f"✅ Attendance marked for User {user_id} (confidence: {confidence:.2f})")
        return user_id, confidence

def run_camera_loop():
    """Live camera attendance system."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not found!")
        return

    print("🎥 Camera started. Press 'q' to quit.")
    print("📱 Face detected → Auto attendance marked!")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Mirror mode

        # Process frame asynchronously
        user_id, confidence = asyncio.run(process_frame_and_mark(frame))

        # Draw status
        status = f"User {user_id} ({confidence:.2f})" if user_id else "No match"
        color = (0, 255, 0) if user_id else (0, 0, 255)
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("YOLO Attendance System - Production", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()