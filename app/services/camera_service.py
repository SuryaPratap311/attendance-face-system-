# app/services/camera_service.py
import subprocess
import sys
import tempfile
import os
import cv2


def capture_frame_from_camera():
    # Save captured frame to a temp file then return it
    tmp_path = tempfile.mktemp(suffix=".jpg")
    script_path = tempfile.mktemp(suffix=".py")

    script = f"""
import cv2
import time
import sys

cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def _is_face_inside_box(face_rect, box):
    fx, fy, fw, fh = face_rect
    bx, by, bw, bh = box
    cx = fx + fw // 2
    cy = fy + fh // 2
    return bx < cx < bx + bw and by < cy < by + bh

OUT_PATH = r"{tmp_path}"

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("Camera open failed")
    sys.exit(1)

for _ in range(10):
    cap.read()

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
bw, bh = int(w * 0.4), int(h * 0.55)
bx, by = (w - bw) // 2, (h - bh) // 2
target_box = (bx, by, bw, bh)

green_since = None
captured = None

while captured is None:
    ret, frame = cap.read()
    if not ret:
        break

    display = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    face_in_box = False
    if len(faces) > 0:
        largest = max(faces, key=lambda f: f[2] * f[3])
        if _is_face_inside_box(largest, target_box):
            face_in_box = True
            fx, fy, fw, fh = largest
            cv2.rectangle(display, (fx, fy), (fx + fw, fy + fh), (255, 255, 0), 2)

    box_color = (0, 255, 0) if face_in_box else (0, 0, 255)  # Green if face in box, else Red
    cv2.rectangle(display, (bx, by), (bx + bw, by + bh), box_color, 3)

    if face_in_box:
        if green_since is None:
            green_since = time.time()
        elapsed = time.time() - green_since
        cv2.putText(
            display,
            f"Hold still... {{max(0, 2 - elapsed):.1f}}s",
            (bx, by - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            box_color,
            2
        )
        if elapsed >= 2:
            cv2.imwrite(OUT_PATH, frame)
            cv2.putText(
                display,
                "CAPTURED!",
                (w // 2 - 80, h // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                box_color,
                3
            )
            captured = True
    else:
        green_since = None
        cv2.putText(
            display,
            "Align face in box",
            (bx, by - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    cv2.imshow("Face Registration", display)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
"""

    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script)

    # Execute in a separate process (GUI window will open in user desktop)
    try:
        proc = subprocess.run(
            [sys.executable, script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        pass
    finally:
        if os.path.exists(script_path):
            os.unlink(script_path)

    if os.path.exists(tmp_path):
        frame = cv2.imread(tmp_path)
        os.unlink(tmp_path)
        return frame

    return None