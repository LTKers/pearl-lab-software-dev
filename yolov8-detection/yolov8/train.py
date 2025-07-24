import os
from ultralytics import YOLO

# load model
model = YOLO("yolov8n.pt")

# train model
print(os.getcwd())

path=os.path.join(os.getcwd(),"config.yaml")
model.train(
    data=path,
    imgsz=1024,
    epochs=10,
    batch=16,
    project="runs/detect",
    augment=True,
    close_mosaic=10,
    patience=20,
    workers=4
)