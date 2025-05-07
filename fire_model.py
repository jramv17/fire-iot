# fire_model.py
from ultralytics import YOLO
import time
import cv2

def detect_fire(timeout=30):
    model = YOLO('best.pt')
    cap = cv2.VideoCapture(0)
    start_time = time.time()

    fire_detected = False

    while time.time() - start_time < timeout:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, imgsz=640, conf=0.6)
        for r in results:
            if r.names and any("fire" in r.names.get(cls_id, "").lower() for cls_id in r.boxes.cls.tolist()):
                fire_detected = True
                break

        if fire_detected:
            break

    cap.release()
    cv2.destroyAllWindows()
    return fire_detected
