import numpy as np

import os

import hashlib
import json


import streamlit as st
import tempfile

from video_analysys import VideoAnalysys
from analysis import analyze_keypoints
from utilities.video_utilitiy import VideoUtility

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
            
    if st.session_state["anon_user"]:
        if st.sidebar.button("Login"):
            st.session_state["page"] = "login"
        
        if st.sidebar.button("Sign Up"):
            st.session_state["page"] = "signup"
            
    else:
        st.sidebar.markdown(
            f"<h3>Logged in as<br>{st.session_state['user'].email}</h3>",
            unsafe_allow_html=True
        )
        if st.sidebar.button("History"):
            st.session_state["page"] = "history"
        if st.sidebar.button("Log Out"):
            st.session_state.clear()


    if st.session_state["page"] == "login":
        render_login_page()
        return

    elif st.session_state["page"] == "signup":
        render_signup_page()
        return    

    elif st.session_state["page"] == "history":
        render_history()
        return
    
    elif st.session_state["page"] == "analysis":
        render_analysis_page()
        return



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
    
    frames, video_keypoints = va.analyze_video(video)
    
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
    
    video_bytes = video.get_video_bytes(frames, video.fps)
    st.video(video_bytes)
    
    existing = (
        supabase
        .table("data_points")
        .select("id")
        .eq("video_hash", video_hash)
        .eq("user_id", st.session_state["user"].id)
        .execute()
        )
    
    if existing.data == []:
        result = supabase.table("data_points").insert({
            "location_points": named_keypoints,
            "name": video_file.name,
            "user_id": st.session_state["user"].id,
            "video_hash": video_hash,
            "left_handed": left_handed,
            "fps": video.fps
        }).execute()
        
        supabase.storage.from_("videos").upload(f"{result.data[0]['id']}", video_bytes)
    
    analyze_keypoints(named_keypoints, left_handed, va, video.fps)
    

def render_history():
    st.title("History")
    
    if st.button("Return to analysis page"):
        st.session_state["page"] = "analysis"
        
    history = (
        supabase
        .table("data_points")
        .select("*")
        .eq("user_id", st.session_state["user"].id)
        .order("created_at", desc=True)
        .execute()
        )
        
    for history_item in history.data:
        if st.button(history_item["name"]):
            video_bytes = supabase.storage.from_("videos").download(f"{history_item['id']}")
            st.video(video_bytes)
            va = VideoAnalysys(history_item["left_handed"])
            
            analyze_keypoints(
                history_item["location_points"],
                history_item["left_handed"],
                va,
                history_item["fps"]
            )
    
if __name__ == "__main__":
    main()