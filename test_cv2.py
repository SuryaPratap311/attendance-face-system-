# test_cv2.py
from app.services.camera_service import capture_frame_from_camera

print("==> Starting camera capture test...")
frame = capture_frame_from_camera()
if frame is None:
    print("❌ Camera capture failed")
else:
    print("✅ Frame captured successfully")