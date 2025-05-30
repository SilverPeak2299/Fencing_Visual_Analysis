import numpy as np
import matplotlib.pyplot as plt


def plot_velocity(x_velocity, label, fps):
    """
    Plot x-direction velocity over time.

    Parameters:
        x_velocity (np.ndarray): 1D array of x-direction velocities.
        label (str): Label for the velocity curve.

    Returns:
        matplotlib.figure.Figure
    """
    import matplotlib.pyplot as plt
    time = np.arange(len(x_velocity)) / fps

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time, x_velocity, label=f"{label} X-Velocity")
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("X-Velocity (px/s)")
    ax.set_title(f"X-Directional Velocity of {label} Over Time")
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
