from ultralytics import YOLO

def process_image(image, model):
    results = model(image)
    return results

def load_model():
    model = YOLO("yolo11n-pose.pt")
    return model
