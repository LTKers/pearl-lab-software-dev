import cv2 as cv
import os
from ultralytics import YOLO

cap=cv.VideoCapture(0)

# load model
model_path=os.path.join("runs", "detect", "train", "weights", "best.pt")
model=YOLO(model_path)
model.conf = 0.01 

threshold=0.0

while True:
    ret, frame=cap.read()

    if ret:
        frame = cv.resize(frame, (1024, 1024))
        results=model(frame)[0]

        for result in results.boxes.data.tolist():
            print("hi")

            x1, y1, x2, y2, score, class_id=result

            if score>threshold:
                cv.rectangle(frame, (int(x1), int(y1)), (int (x2), int(y2)), (0,255,0), 4)

        if cv.waitKey(1)&0xFF==ord('q'):
            break
        
        cv.imshow("Yolo Test", frame)


cap.release()
cv.destroyAllWindows()



