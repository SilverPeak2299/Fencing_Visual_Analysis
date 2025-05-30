# Fencing Visual Analysis

**Fencing Visual Analysis** is an end-to-end data processing and visualization tool designed to extract insights from fencing performance using computer vision. Built as a software engineering project with a focus on data engineering principles, the app demonstrates how raw video data can be transformed into structured, meaningful analytics for sports performance analysis.

**Live demo:**  
[https://fencing-visual-analysis.streamlit.app/](https://fencing-visual-analysis.streamlit.app/)

## Project Overview

This project was developed to explore the application of key data engineering concepts, including:

- **Data ingestion** from unstructured sources (video files)
- **Transformation pipelines** using pose estimation models
- **Storage and structuring** of time-series joint coordinates
- **Visualization** of multi-dimensional movement trajectories
- **Deployment** of a lightweight, interactive analytics interface

The app serves as a tool for athletes and coaches to analyze fencing technique by visualizing the motion of key joints over time.

## Key Features

- Upload fencing footage and automatically extract joint positions
- Visualize trajectories of shoulders, hips, wrists, and more
- Plot movement paths, velocity changes, and side-by-side comparisons
- Designed for repeated use in training environments and performance reviews
- Downloadable visual outputs for offline analysis or reporting

## Target Skills Demonstrated

- Python scripting for video frame extraction and data manipulation
- Integration of computer vision models
- Development of a reproducible data pipeline for pose estimation
- Visualization with matplotlib
- Deployment using Streamlit and version control with Git
- Lightweight system design with scalability in mind

## How It Works

1. A user uploads a fencing video (MP4 format recommended)
2. The app uses a pose estimation backend to extract joint coordinates
3. Joint positions are tracked across frames and structured into a time series
4. The user selects joints of interest and views trajectory plots
5. Visualizations can be exported for further analysis

## Technology Stack

- **Frontend/UI**: Streamlit  
- **Computer Vision**: YOLO11 Pose 
- **Data Handling**: pandas, NumPy  
- **Visualization**: matplotlib 
- **Deployment**: Streamlit Cloud  

## Running Locally

Clone the repository:

```bash
git clone https://github.com/SilverPeak2299/Fencing_lunge_analysys.git
cd fencing-lunge-analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

