
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import os
import uuid

model = YOLO("best.pt")  

def detect_fire_static(image_path):
    results = model(image_path)[0]

    fire_detected = False
    fire_percentage = 0
    fire_areas = []

    image = cv2.imread(image_path)
    h, w, _ = image.shape

    for box in results.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].cpu().numpy().astype(int)

        label = results.names[cls_id].lower()
        if "fire" in label:  
            fire_detected = True
            x1, y1, x2, y2 = xyxy
            area = (x2 - x1) * (y2 - y1)
            fire_areas.append(area)

            # Draw bounding box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    total_fire_area = sum(fire_areas)
    fire_percentage = (total_fire_area / (w * h)) * 100 if fire_areas else 0

    output_filename = f"{uuid.uuid4().hex}.jpg"
    output_path = os.path.join("static/results", output_filename)
    cv2.imwrite(output_path, image)

    return {
        "fire_detected": fire_detected,
        "fire_percentage": round(fire_percentage, 2),
        "image_path": output_path
    }