from altair.vegalite.v5.api import renderers
import numpy as np

import os

import hashlib
import json

import streamlit as st
import tempfile

from video_analysys import VideoAnalysys
from utilities.video_utilitiy import VideoUtility
from utilities.plots import plot_keypoint_trajectories, plot_velocity
from utilities.filters import lowpass_filter

import cv2

from supabase import Client, create_client

SUPABASE_URL = os.environ.get("FENCING_VISION_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("FENCING_VISION_SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "analysis"
    
    if st.session_state.get("user") is None:
        response = supabase.auth.sign_in_anonymously()
        st.session_state["user"] = response.user
        st.session_state["anon_user"] = True
    st.sidebar.title("Fencing Video Analysys")
    
    if st.session_state.get("anon_user"):
        st.sidebar.warning("You are using an anonymous account. Please sign up or log in to save your data.")
            

    if st.sidebar.button("Login"):
        st.session_state["page"] = "login"
        
    if st.sidebar.button("Sign Up"):
        st.session_state["page"] = "signup"
        
    if st.sidebar.button("Log Out"):
        st.session_state.clear()
        st.rerun()


    if st.session_state["page"] == "login":
        render_login_page()
        st.rerun()
        return
    elif st.session_state["page"] == "signup":
        render_signup_page()
        st.rerun()
        return    

    render_analysis_page()
    


def render_signup_page():
    st.title("Fencing Video Analysis Sign Up Page")
    email = st.text_input("Email: ")
    password = st.text_input("Password: ", type="password")
    
    signup_button = st.button("Log In", key= "submitting_user")

    try:
        if signup_button:
            response = supabase.auth.update_user(
                {
                    "email": email,
                    "password": password
                }
                )
                
            if response.user is not None:
                st.session_state["user"] = response.user
                st.session_state["anon_user"] = False
                st.session_state["page"] = "analysis"
                st.rerun()
            else:
                st.error("Invalid email or password.")
                
    except Exception as e:
        st.error(f"{e}")

def render_login_page():
        
    email = st.text_input("Email: ")
    password = st.text_input("Password: ", type="password")
    
    login_button = st.button("Log In", key= "submitting_user")

    try:
        if login_button:
            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
                )
                
            if response.user is not None:
                st.session_state["user"] = response.user
                st.session_state["anon_user"] = False
                st.session_state["page"] = "analysis"
                st.rerun()
            else:
                st.error("Invalid email or password.")
        
    except Exception as e:
        st.error(f"{e}")
    
def render_analysis_page():
    st.title("Fencing Lunge Analysis")
    left_handed = st.checkbox("Left Handed? ")
    video_file = st.file_uploader("Upload a fencing video", type=["mp4"])
    if video_file is None:
        st.error("Please upload a mp4 file.")
        return
    
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(video_file.read())
        
    video = VideoUtility(temp_file.name)
    va = VideoAnalysys(left_handed)
    
    frame_exists, frame = video.get_frame()
    
    frames = []
    video_keypoints = []
    
    while frame_exists:
        
        processed_frame = va.analyze_frame(frame)
        results = processed_frame
        
        if len(results[0].keypoints) == 0:
            frame_exists, frame = video.get_frame()
            continue  # No person detected
        
        keypoints = results[0].keypoints.xy[0].cpu().numpy()  # First person only
        keypoint_list = keypoints.tolist()
        video_keypoints.append(keypoint_list)
        
        # Plot keypoints on frame
        processed_frame = results[0].plot()
        frames.append(processed_frame)
        
        frame_exists, frame = video.get_frame()
    
    
    keypoint_names = [
            "nose", "left_eye", "right_eye", "left_ear", "right_ear",
            "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
            "left_wrist", "right_wrist", "left_hip", "right_hip",
            "left_knee", "right_knee", "left_ankle", "right_ankle"
        ]
        
    keypoints_array = np.array(video_keypoints)
    
    named_keypoints = {
        name: keypoints_array[:, idx, :].tolist()
        for idx, name in enumerate(keypoint_names)
    }
    
    video_hash = hashlib.sha256(json.dumps(named_keypoints).encode()).hexdigest()
    
    existing = (
        supabase
        .table("data_points")
        .select("id")
        .eq("video_hash", video_hash)
        .eq("user_id", st.session_state["user"].id)
        .execute()
    )
    
    if existing.data == []:
        supabase.table("data_points").insert({
            "location_points": named_keypoints,
            "name": video_file.name,
            "user_id": st.session_state["user"].id,
            "video_hash": video_hash
        }).execute()
    
    
    # Convert frames to video
    h, w, _ = frames[0].shape
    fps = video.fps
    output_path = tempfile.NamedTemporaryFile(suffix=".avi", delete=False).name
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    for frame in frames:
        writer.write(frame)

    writer.release()

    st.video(output_path)
    
    
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
    wrist_velocity = va.compute_velocity(wrist_path, video.fps)
    filtered_wrist_velocity = lowpass_filter(wrist_velocity)
    fig = plot_velocity(filtered_wrist_velocity, "Wrist", video.fps)
    st.pyplot(fig)

    left_shoulder_velocity = va.compute_velocity(left_shoulder_path, video.fps)
    filtered_left_shoulder_velocity = lowpass_filter(left_shoulder_velocity)
    fig = plot_velocity(filtered_left_shoulder_velocity, "Left Shoulder", video.fps)
    st.pyplot(fig)
    
    left_hip_velocity = va.compute_velocity(left_hip_path, video.fps)
    filtered_left_hip_velocity = lowpass_filter(left_hip_velocity)
    fig = plot_velocity(filtered_left_hip_velocity, "Left Hip", video.fps)
    st.pyplot(fig)
    
    
    wrist_hip_delta = filtered_wrist_velocity - filtered_left_hip_velocity
    fig = plot_velocity(wrist_hip_delta, "Wrist Velocity - Hip Velocity", video.fps)
    st.pyplot(fig)
    
    # st.subheader("Accelerations")
    # left_hip_acceleration = va.compute_acceleration(left_hip_velocity, video.fps)
    # filtered_left_hip_acceleration = lowpass_filter(left_hip_acceleration)
    # fig = plot_velocity(filtered_left_hip_acceleration, "Left Hip", video.fps)
    # st.pyplot(fig)
    
    # st.subheader("Duration")
    # result = va.estimate_motion_time(filtered_left_hip_acceleration, video.fps)
    # st.write(f"Estimated motion time: {result["duration"]} seconds")


if __name__ == "__main__":
    main()