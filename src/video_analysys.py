from ultralytics import YOLO
import numpy as np
import streamlit as st


class VideoAnalysys:
    model: YOLO
    left_handed: bool
    
    def __init__(self, left_handed=False) :
        self.model = YOLO("./models/yolo11n-pose.pt")
        self.left_handed = left_handed
        
    def analyze_frame(self, frame):
        results = self.model(frame)
        return results
        
    @st.cache_data(show_spinner="Processing video...", max_entries=10) 
    def analyze_video(_self, _video):
        frame_exists, frame = _video.get_frame()
        
        frames = []
        video_keypoints = []
    
        while frame_exists:
            
            processed_frame = _self.analyze_frame(frame)
            results = processed_frame
            
            if len(results[0].keypoints) == 0:
                frame_exists, frame = _video.get_frame()
                continue  # No person detected
            
            keypoints = results[0].keypoints.xy[0].cpu().numpy()  # First person only
            keypoint_list = keypoints.tolist()
            video_keypoints.append(keypoint_list)
            
            # Plot keypoints on frame
            processed_frame = results[0].plot()
            frames.append(processed_frame)
            
            frame_exists, frame = _video.get_frame()
            
        return frames, video_keypoints


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
        
        #Flipping over x axis for consistency
        if not self.left_handed:
            x_velocity *= -1
            
        return x_velocity
        
    def compute_acceleration(self, x_velocity, fps):
        """
        Compute x-direction acceleration from velocity over time.
    
        Parameters:
            x_velocity (np.ndarray): 1D array of x-direction velocities (pixels/frame).
            fps (int): Frames per second of the video.
    
        Returns:
            np.ndarray: 1D array of x accelerations (N-1 values).
        """
        dv = np.diff(x_velocity)  # Change in velocity per frame
        x_acceleration = dv * fps  # Convert to units per second
        
        return x_acceleration
        
    
    def estimate_motion_time(self, x_acceleration, fps, acc_threshold=750):
        """
        Estimate start and end time of motion based on x-direction velocity.
    
        Parameters:
            x_velocity (np.ndarray): 1D array of x-direction velocities (pixels/frame).
            fps (int): Frames per second of the video.
            acc_threshold (float): Threshold to detect significant acceleration.

    
        Returns:
            dict: {
                'start_time': Time in seconds when motion starts,
                'end_time': Time in seconds when motion ends,
                'duration': Duration of motion in seconds,
                'start_idx': Start frame index,
                'end_idx': End frame index
            }
        """
        # Find start of motion
        start_idx = np.argmax(np.abs(x_acceleration) > acc_threshold)
    
        # Find end of motion
        end_idx_candidates = np.where(np.abs(x_acceleration[start_idx:]) < acc_threshold)[0]
        if len(end_idx_candidates) > 0:
            end_idx = start_idx + end_idx_candidates[0]
        else:
            end_idx = len(x_acceleration) - 1
    
        # Convert indices to time
        start_time = start_idx / fps
        end_time = end_idx / fps
        duration = end_time - start_time
    
        return {
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration,
            'start_idx': start_idx,
            'end_idx': end_idx
        }
