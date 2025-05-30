import numpy as np

import streamlit as st
import tempfile

from video_analysys import VideoAnalysys
from utilities.video_utilitiy import VideoUtility
from utilities.plots import plot_keypoint_trajectories, plot_velocity
from utilities.filters import lowpass_filter

def main():
    st.title("Fencing Lunge Analysis")
    video_file = st.file_uploader("Upload a fencing video", type=["mp4"])
    
    if video_file is None:
        st.error("Please upload a mp4 file.")
        return
    
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())
    
    video = VideoUtility(temp_file.name)
    va = VideoAnalysys()
    
    left_hip_path = []
    right_hip_path = []
    left_shoulder_path = []
    right_wrist_path = []
    
    video_placeholder = st.empty()
    
    frame_exists, frame = video.get_frame()
    while frame_exists:
        
        processed_frame = va.analyze_frame(frame)
        results = processed_frame
        
        if len(results[0].keypoints) == 0:
            continue  # No person detected
        
        keypoints = results[0].keypoints.xy[0].cpu().numpy()  # First person only
        
        # Append coordinates (x, y)
        left_hip_path.append(keypoints[11])       # Left hip
        right_hip_path.append(keypoints[12])      # Right hip
        left_shoulder_path.append(keypoints[6])   # Left shoulder
        right_wrist_path.append(keypoints[10])     # Right wrist
        
        # Plot keypoints on frame
        processed_frame = results[0].plot()
        
        # Show the result
        video_placeholder.image(processed_frame, caption="Pose Tracking")
        
        frame_exists, frame = video.get_frame()
    

    lh = lowpass_filter(np.array(left_hip_path))
    rh = lowpass_filter(np.array(right_hip_path))
    ls = lowpass_filter(np.array(left_shoulder_path))
    re = lowpass_filter(np.array(right_wrist_path))
    

    st.subheader("Pose Keypoint Trajectories")
    fig = plot_keypoint_trajectories(
        ("Left Hip", lh),
        ("Right Hip", rh),
        ("Left Shoulder", ls),
        ("Right wrist", re)
    )
    st.pyplot(fig)
    
    
    st.header("Velocities")
    wrist_velocity = va.compute_velocity(right_wrist_path, video.fps)
    filtered_wrist_velocity = lowpass_filter(wrist_velocity)
    fig = plot_velocity(filtered_wrist_velocity, "Right Wrist")
    st.pyplot(fig)

    left_shoulder_velocity = va.compute_velocity(left_shoulder_path, video.fps)
    filtered_left_shoulder_velocity = lowpass_filter(left_shoulder_velocity)
    fig = plot_velocity(filtered_left_shoulder_velocity, "Left Shoulder")
    st.pyplot(fig)
    
    left_hip_velocity = va.compute_velocity(left_hip_path, video.fps)
    filtered_left_hip_velocity = lowpass_filter(left_hip_velocity)
    fig = plot_velocity(filtered_left_hip_velocity, "Left Hip")
    st.pyplot(fig)


if __name__ == "__main__":
    main()