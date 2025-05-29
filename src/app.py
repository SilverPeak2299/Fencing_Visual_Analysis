import argparse
import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt

from yolo_pose import process_image, load_model

def main():
    file = return_file_path()
    
    video = cv.VideoCapture(file)
    
    left_hip_path = []
    right_hip_path = []
    left_shoulder_path = []
    right_wrist_path = []
    
    while video.isOpened():
        yolo_model = load_model()
        ret, frame = video.read()
        if not ret:
            break
        
        # Inference
        results = process_image(frame, yolo_model)
        
        if len(results[0].keypoints) == 0:
            continue  # No person detected
        
        keypoints = results[0].keypoints.xy[0].cpu().numpy()  # First person only
        
        # Append coordinates (x, y)
        left_hip_path.append(keypoints[11])       # Left hip
        right_hip_path.append(keypoints[12])      # Right hip
        left_shoulder_path.append(keypoints[6])   # Left shoulder
        right_wrist_path.append(keypoints[10])     # Right wrist
        
        # Plot keypoints on frame
        annotated_frame = results[0].plot()
        
        # Show the result
        cv.imshow("Fencing Pose Tracking", annotated_frame)
        
        # Exit on ESC
        if cv.waitKey(1) == 27:
            break
    

    lh = np.array(left_hip_path)
    rh = np.array(right_hip_path)
    ls = np.array(left_shoulder_path)
    re = np.array(right_wrist_path)
    
    # Plot
    plot_keypoint_trajectories(
        ("Left Hip", lh),
        ("Right Hip", rh),
        ("Left Shoulder", ls),
        ("Right wrist", re)
    )

def plot_keypoint_trajectories(*keypoints):
    """
    Plot 2D trajectories of any number of keypoints.

    Parameters:
        keypoints: Any number of tuples in the form (label: str, coords: np.ndarray)
                   where coords is an Nx2 array of (x, y) points.
    """
    plt.figure(figsize=(10, 6))

    for label, coords in keypoints:
        coords = np.array(coords)
        if coords.shape[1] != 2:
            raise ValueError(f"{label} must be an Nx2 array of (x, y) coordinates.")
        plt.plot(coords[:, 0], coords[:, 1], label=label)

    plt.gca().invert_yaxis()  # OpenCV-style image coordinates
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Pose Keypoint Trajectories")
    plt.legend()
    plt.grid(True)
    plt.show()

def return_file_path():
    parser = argparse.ArgumentParser(description='Return file path')
    parser.add_argument('file_path', type=str, help='Path to the file')
    args = parser.parse_args()
    return args.file_path
 
if __name__ == "__main__":
    main()