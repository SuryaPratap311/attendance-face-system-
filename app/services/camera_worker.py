import cv2
from ultralytics import YOLO
from app.core.config import settings

model = YOLO(settings.yolo_model_path)

def run_camera_loop():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = model.predict(source=frame, verbose=False)
        annotated = results[0].plot() if results else frame

        cv2.imshow("YOLO Attendance POC", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()