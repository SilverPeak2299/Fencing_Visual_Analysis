import numpy as np
import streamlit as st

from utilities.plots import plot_keypoint_trajectories, plot_velocity
from utilities.filters import lowpass_filter


def analyze_keypoints(named_keypoints, left_handed, va, fps):
    left_hip_path = named_keypoints["left_hip"] 
    right_hip_path = named_keypoints["right_hip"]
    left_shoulder_path = named_keypoints["left_shoulder"]
    
    if left_handed:
        wrist_path = named_keypoints["left_wrist"] 
    else:
        wrist_path = named_keypoints["right_wrist"]
    
    lh = lowpass_filter(np.array(left_hip_path))
    rh = lowpass_filter(np.array(right_hip_path))
    ls = lowpass_filter(np.array(left_shoulder_path))
    wr = lowpass_filter(np.array(wrist_path))
    

    st.subheader("Pose Keypoint Trajectories")
    fig = plot_keypoint_trajectories(
        ("Left Hip", lh),
        ("Right Hip", rh),
        ("Left Shoulder", ls),
        ("wrist", wr)
    )
    st.pyplot(fig)
    
    st.header("Velocities")
    wrist_velocity = va.compute_velocity(wrist_path, fps)
    filtered_wrist_velocity = lowpass_filter(wrist_velocity)
    fig = plot_velocity(filtered_wrist_velocity, "Wrist", fps)
    st.pyplot(fig)

    left_shoulder_velocity = va.compute_velocity(left_shoulder_path, fps)
    filtered_left_shoulder_velocity = lowpass_filter(left_shoulder_velocity)
    fig = plot_velocity(filtered_left_shoulder_velocity, "Left Shoulder", fps)
    st.pyplot(fig)
    
    left_hip_velocity = va.compute_velocity(left_hip_path, fps)
    filtered_left_hip_velocity = lowpass_filter(left_hip_velocity)
    fig = plot_velocity(filtered_left_hip_velocity, "Left Hip", fps)
    st.pyplot(fig)
    
    
    wrist_hip_delta = filtered_wrist_velocity - filtered_left_hip_velocity
    fig = plot_velocity(wrist_hip_delta, "Wrist Velocity - Hip Velocity", fps)
    st.pyplot(fig)
    
    shoulder_hip_delta = filtered_left_shoulder_velocity - filtered_left_hip_velocity
    fig = plot_velocity(shoulder_hip_delta, "Shoulder Velocity - Hip Velocity", fps)
    st.pyplot(fig)
    
    # st.subheader("Accelerations")
    # left_hip_acceleration = va.compute_acceleration(left_hip_velocity, fps)
    # filtered_left_hip_acceleration = lowpass_filter(left_hip_acceleration)
    # fig = plot_velocity(filtered_left_hip_acceleration, "Left Hip", fps)
    # st.pyplot(fig)
    
    # st.subheader("Duration")
    # result = va.estimate_motion_time(filtered_left_hip_acceleration, fps)
    # st.write(f"Estimated motion time: {result["duration"]} seconds")
