import os
from ultralytics import YOLO

# load model
model = YOLO("yolov8n.pt")

# train model
config = os.path.join("YOLOV8", "config.yaml")
results = model.train(data=config, epochs=1)