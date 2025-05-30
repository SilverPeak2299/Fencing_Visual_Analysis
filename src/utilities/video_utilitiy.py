import cv2 as cv

class VideoUtility:
    fps: int
    video_length: float
    video: cv.VideoCapture
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.video = cv.VideoCapture(file_path)
        
        self.fps = int(self.video.get(cv.CAP_PROP_FPS))
        self.video_length = self.video.get(cv.CAP_PROP_FRAME_COUNT) / self.fps
        
    def get_frame(self):
        ret, frame = self.video.read()
        return ret, frame