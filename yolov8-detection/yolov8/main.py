import cv2 as cv
import os
from ultralytics import YOLO

cap=cv.VIDEOCapture(0)

# load model
model_path=os.path.join("runs", "weights", "best.pt")
model=YOLO(model_path)

while True:
    ret, frame=cap.read()

    if ret:
        pass


