from ultralytics import YOLO
import numpy as np
from scipy.signal import savgol_filter

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
            
    def lowpass_filter(self, trajectory, window_length=13, polyorder=2):
        """
        Smooth 2D trajectory data using Savitzky-Golay filter.
        
        Parameters:
            trajectory (np.ndarray): Nx2 array of (x, y) coordinates.
            window_length (int): Number of frames in smoothing window (must be odd).
            polyorder (int): Polynomial order to fit.
    
        Returns:
            np.ndarray: Smoothed trajectory of shape Nx2.
        """
        if len(trajectory) < window_length:
            return trajectory  # Not enough points to smooth
        smoothed = np.zeros_like(trajectory)
        smoothed[:, 0] = savgol_filter(trajectory[:, 0], window_length, polyorder)
        smoothed[:, 1] = savgol_filter(trajectory[:, 1], window_length, polyorder)
        return smoothed