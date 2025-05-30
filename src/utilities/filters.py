from scipy.signal import savgol_filter
import numpy as np

def lowpass_filter(trajectory, window_length=13, polyorder=2):
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
    
    if trajectory.ndim == 2:
        smoothed[:, 0] = savgol_filter(trajectory[:, 0], window_length, polyorder)
        smoothed[:, 1] = savgol_filter(trajectory[:, 1], window_length, polyorder)
    
    elif trajectory.ndim == 1:
       smoothed = savgol_filter(trajectory, window_length, polyorder) 
    
    return smoothed