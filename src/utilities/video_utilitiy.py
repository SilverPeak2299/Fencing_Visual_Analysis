import cv2 as cv
import imageio
import tempfile
import os

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
    
    def compress_frames(self, frames: list):
        compressed_frames = []
        for frame in frames:
            compressed_frame = cv.imencode('.jpg', frame)[1].tobytes()
            compressed_frames.append(compressed_frame)

        return compressed_frames
        
    from io import BytesIO
    
    def get_video_bytes(self, frames, fps=30):
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
            tmp_path = tmpfile.name
    
        writer = imageio.get_writer(tmp_path, format='ffmpeg', mode='I', fps=fps)
        for frame in frames:
            writer.append_data(frame)
        writer.close()
    
        with open(tmp_path, "rb") as f:
            video_bytes = f.read()
        
        os.remove(tmp_path)
        
        return video_bytes
    