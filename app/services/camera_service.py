import cv2

def capture_frame_from_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    for _ in range(10):
        cap.read()

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return None

    return frame