import cv2 as cv
import os
from ultralytics import YOLO

cap = cv.VideoCapture(0)

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "runs", "detect", "train", "weights", "best.pt")
model = YOLO(model_path)
model.conf = 0.01  


threshold = 0.0  

while True:
    ret, frame = cap.read()
    
    if not ret:
        break

    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    results = model(frame_rgb)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result

        if score > threshold:
            cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"{model.names[int(class_id)]} {score:.2f}"
            cv.putText(frame, label, (int(x1), int(y1) - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv.imshow("YOLOv8 Detection", frame)
    print(results.boxes)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
