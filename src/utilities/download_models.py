from ultralytics import YOLO

model = YOLO("models/yolo11n-pose.pt")
model.export(format="onnx")