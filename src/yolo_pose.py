from ultralytics import YOLO

def process_image(image, model):
    results = model(image)
    return results

def load_model():
    model = YOLO("./models/yolo11n-pose.pt")
    return model
