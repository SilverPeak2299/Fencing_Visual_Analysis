from ultralytics import YOLO
import numpy as np

class VideoAnalysys:
    model: YOLO
    
    def __init__(self) :
        self.model = YOLO("./models/yolo11n-pose.pt")
        
    def analyze_frame(self, frame):
        results = self.model(frame)
        return results

    def compute_velocity(self, positions, fps=30):
        """
        Compute x-direction velocity from position coordinates over time.
    
        Parameters:
            positions (np.ndarray): Nx2 array of (x, y) positions.
            fps (int): Frames per second of the video.
    
        Returns:
            np.ndarray: 1D array of x velocities (N-1 values).
        """
        positions = np.array(positions)
        dx = np.diff(positions[:, 0])  # Change in x per frame
        x_velocity = dx * fps  # Convert to units per second
        return x_velocity
            
