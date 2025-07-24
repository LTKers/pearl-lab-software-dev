from ultralytics import YOLO

# load model
model = YOLO("yolov8n.pt")

# train model
results = model.train(data="config.yaml", epochs=1)