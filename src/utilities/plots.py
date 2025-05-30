import numpy as np
import matplotlib.pyplot as plt


def plot_velocity(velocity, label):
    """
    Plot velocity over time.
    
    Parameters:
        velocity (np.ndarray): 1D array of velocity magnitudes.
        label (str): Label for the velocity curve.
    
    Returns:
        matplotlib.figure.Figure
    """
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 4))
    time = np.arange(len(velocity)) / 30  # Time in seconds (assuming 30fps)
    ax.plot(time, velocity, label=f"{label} Velocity")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Velocity (px/s)")
    ax.set_title(f"Velocity of {label} Over Time")
    ax.grid(True)
    ax.legend()
    return fig

def plot_keypoint_trajectories(*keypoints):
    """
    Plot 2D trajectories of any number of keypoints.

    Parameters:
        keypoints: Any number of tuples in the form (label: str, coords: np.ndarray)
                   where coords is an Nx2 array of (x, y) points.
    """

    fig, ax = plt.subplots(figsize=(10, 6))

    for label, coords in keypoints:
        coords = np.array(coords)
        if coords.shape[1] != 2:
            raise ValueError(f"{label} must be an Nx2 array of (x, y) coordinates.")
        ax.plot(coords[:, 0], coords[:, 1], label=label)

    ax.invert_yaxis()  # OpenCV-style image coordinates
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Pose Keypoint Trajectories")
    ax.legend()
    ax.grid(False)

    return fig
