import cv2 as cv
import os
from ultralytics import YOLO

cap=cv.VIDEOCapture(0)

# load model
model_path=os.path.join("YOLOV8", "")
model=YOLO()

while True:
    ret, frame=cap.read()

    if ret:
        pass


