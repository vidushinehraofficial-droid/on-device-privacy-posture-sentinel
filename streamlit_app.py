import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import mediapipe.python.solutions.pose as mp_pose
import mediapipe.python.solutions.face_detection as mp_face
from PIL import Image
import time

# Page Configuration
st.set_page_config(page_title="Privacy & Posture Sentinel", layout="wide")
st.title("🛡️ On-Device Privacy & Posture Sentinel")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    audio_enabled = st.checkbox("📢 Audio Alerts", value=True)
    sensitivity = st.slider("Slouch Sensitivity (°)", 60, 85, 70)
    auto_lock = st.checkbox("🔒 Auto Screen Lock", value=True)
    
    st.divider()
    
    st.info("""
    **How it works:**
    - 📷 Monitors your posture in real-time
    - 👤 Detects if someone else is looking at your screen
    - ⚠️ Alerts you if you're slouching
    - 🔐 Can auto-lock your screen if needed
    """)

# Initialize Models
@st.cache_resource
def load_models():
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=0,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    face_detection = mp_face.FaceDetection(min_detection_confidence=0.6)
    return pose, face_detection

pose_model, face_model = load_models()

def analyze_posture(frame, pose, sensitivity_angle=70):
    """Analyze posture from frame"""
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)
    
    status = "✅ Good Posture"
    angle = 0.0
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        ear_lm = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        shoulder_lm = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        
        ear = [ear_lm.x, ear_lm.y]
        shoulder = [shoulder_lm.x, shoulder_lm.y]
        
        ear_px = (int(ear[0] * w), int(ear[1] * h))
        shoulder_px = (int(shoulder[0] * w), int(shoulder[1] * h))
        
        radians = np.arctan2(shoulder[1] - ear[1], shoulder[0] - ear[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        if angle < sensitivity_angle or angle > 110:
            status = "⚠️ Slouching Detected!"
            line_color = (0, 0, 255)  # Red
        else:
            line_color = (0, 255, 0)  # Green
        
        cv2.line(frame, ear_px, shoulder_px, line_color, 3)
        cv2.circle(frame, ear_px, 6, line_color, -1)
        cv2.circle(frame, shoulder_px, 6, line_color, -1)
    
    return status, angle, frame

def detect_faces(frame, face_detector):
    """Detect faces and intruders"""
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb_frame)
    
    face_count = 0
    security_status = "✅ Safe"
    
    if results.detections:
        face_count = len(results.detections)
        
        if face_count > 1:
            security_status = "🚨 INTRUDER DETECTED!"
            box_color = (0, 0, 255)  # Red
        else:
            security_status = "✅ Safe (1 Face)"
            box_color = (0, 255, 0)  # Green
        
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            xmin = int(bboxC.xmin * w)
            ymin = int(bboxC.ymin * h)
            box_width = int(bboxC.width * w)
            box_height = int(bboxC.height * h)
            
            cv2.rectangle(frame, (xmin, ymin), (xmin + box_width, ymin + box_height), box_color, 2)
            
            label = "User" if face_count == 1 else "INTRUDER!"
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)
    
    return security_status, face_count, frame

# Main Layout
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📹 Live Feed")
    video_placeholder = st.empty()
    frame_placeholder = st.empty()

with col2:
    st.subheader("📊 Dashboard")
    posture_placeholder = st.empty()
    security_placeholder = st.empty()
    stats_placeholder = st.empty()

# Camera Stream
st.write("Starting camera... Please allow camera access when prompted.")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("❌ Unable to access camera. Please check your camera settings.")
else:
    start_time = time.time()
    total_frames = 0
    slouch_frames = 0
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            st.error("❌ Failed to read frame from camera")
            break
        
        # Flip frame for selfie view
        frame = cv2.flip(frame, 1)
        
        # Analyze posture
        posture_status, angle, frame = analyze_posture(frame, pose_model, sensitivity)
        
        # Detect intruders
        security_status, face_count, frame = detect_faces(frame, face_model)
        
        # Update counters
        total_frames += 1
        if "Slouching" in posture_status:
            slouch_frames += 1
        
        # Calculate session stats
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        score = max(0, 100 - (slouch_frames / total_frames * 100)) if total_frames > 0 else 100
        
        # Convert frame to RGB for display
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Update displays
        with col1:
            video_placeholder.image(frame_rgb, use_column_width=True)
        
        with col2:
            with posture_placeholder.container():
                st.metric(label="Posture Status", value=posture_status, delta=f"{angle:.1f}°")
            
            with security_placeholder.container():
                st.metric(label="Security", value=security_status, delta=f"{face_count} face(s)")
            
            with stats_placeholder.container():
                st.metric(label="Posture Score", value=f"{score:.1f}%")
                st.metric(label="Session Duration", value=f"{minutes}m {seconds}s")
        
        # Small delay to prevent overwhelming the browser
        time.sleep(0.03)
        
        # Optional: Add a stop button
        if st.button("Stop Monitoring", key="stop_button"):
            break

cap.release()
st.success("✅ Monitoring stopped")
