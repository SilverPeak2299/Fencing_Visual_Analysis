from ultralytics import YOLO
import numpy as np
from scipy.signal import savgol_filter

class VideoAnalysys:
    model: YOLO
    
    def __init__(self) :
        self.model = YOLO("./models/yolo11l-pose.pt")
        
    def analyze_frame(self, frame):
        results = self.model(frame)
        return results

    def compute_velocity(self, positions, fps=30):
        """
        Compute velocity magnitude from position coordinates over time.
        
        Parameters:
            positions (np.ndarray): Nx2 array of (x, y) positions.
            fps (int): Frames per second of the video.
    
        Returns:
            np.ndarray: Array of velocity magnitudes per frame (N-1 values).
        """
        positions = np.array(positions)
        deltas = np.diff(positions, axis=0)  # Compute differences between frames
        speeds = np.linalg.norm(deltas, axis=1)  # Euclidean distance per frame
        velocity = speeds * fps  # Convert to units per second
        return velocity
        
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