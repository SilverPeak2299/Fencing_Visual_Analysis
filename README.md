# Fencing Visual Analysis

**Fencing Visual Analysis** is an end-to-end data processing and visualization tool designed to extract insights from fencing performance using computer vision. Built as a software engineering project with a focus on data engineering principles, the app demonstrates how raw video data can be transformed into structured, meaningful analytics for sports performance analysis.

**Live demo:**  
[https://fencing-computer-vision-analysis.streamlit.app/](https://fencing-computer-vision-analysis.streamlit.app/)

## Project Overview

This project was developed to explore the application of key data engineering concepts, including:

- **Data ingestion** from unstructured sources (video files)
- **Transformation pipelines** using pose estimation models
- **Storage and structuring** of time-series joint coordinates
- **Visualization** of multi-dimensional movement trajectories
- **Deployment** of a lightweight, interactive analytics interface

The app serves as a tool for athletes and coaches to analyze fencing technique by visualizing the motion of key joints over time.

## Key Features

- **User Authentication**: Secure access through Supabase's authentication services.
- **Video Upload and Storage**: Upload fencing footage, which is stored in Supabase storage buckets for efficient retrieval.
- **Pose Estimation**: Automatically extract joint positions using YOLOv11 Pose.
- **Data Persistence**: Computed location points are stored in a Supabase database, enabling persistent data tracking.
- **Visualization Tools**: Visualize trajectories of shoulders, hips, wrists, and more; plot movement paths, velocity changes, and side-by-side comparisons.
- **History Page**: View and manage previously uploaded videos and corresponding analyses.

## Target Skills Demonstrated

- Python scripting for video frame extraction and data manipulation
- Integration of computer vision models
- Development of a reproducible data pipeline for pose estimation
- Visualization with matplotlib
- Deployment using Streamlit and version control with Git
- Lightweight system design with scalability in mind
- Integration with Supabase for authentication, database, and storage solutions

## Technology Stack

- **Frontend/UI**: Streamlit  
- **Computer Vision**: YOLOv11 Pose 
- **Data Handling**: NumPy  
- **Visualization**: matplotlib 
- **Backend Services**: Supabase (authentication, database, storage)
- **Deployment**: Streamlit Cloud

## Next Steps

Planned future development areas for the project include:

- **Automated Database Maintenance**  
  Implement scheduled background tasks to manage storage and improve efficiency, including:
  - Removing old or inactive anonymous user accounts
  - Deleting outdated video files from Supabase buckets to minimize storage usage

- **Infrastructure Migration**  
  Port the system to a more scalable and performant cloud provider (e.g., AWS, GCP, or Azure) to support more users, improve processing speeds, and enhance reliability.

- **Frontend Overhaul with Next.js**  
  Replace the current Streamlit-based UI with a modern, dedicated frontend using **Next.js**. This will allow for:
  - Improved interactivity and responsiveness
  - More control over styling and layout
  - Separation of concerns between the frontend and backend for better scalability

- **Machine Learning Integration**  
  Use the stored joint position time-series data to train a **neural network**. Potential goals include:
  - Classifying fencing movements or techniques
  - Identifying anomalies or inefficiencies in form
  - Providing real-time feedback or recommendations for athletes

## Running Locally

Clone the repository:

```bash
git clone https://github.com/SilverPeak2299/Fencing_Visual_Analysis.git
cd Fencing_Visual_Analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

