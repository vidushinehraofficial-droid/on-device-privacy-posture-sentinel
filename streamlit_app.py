import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import mediapipe as mp
import mediapipe.solutions.pose as mp_pose
import mediapipe.solutions.face_detection as mp_face

# Page Configuration
st.set_page_config(page_title="Privacy & Posture Sentinel", layout="wide")
st.title("🛡️ On-Device Privacy & Posture Sentinel")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    sensitivity = st.slider("Slouch Sensitivity (°)", 60, 85, 70)
    
    st.divider()
    
    st.info("""
    **How it works:**
    - 📤 Upload an image to analyze
    - 👤 Detects if someone else is looking at your screen
    - ⚠️ Alerts you if you're slouching
    - 🔒 Privacy-focused: No data collection
    """)

# Initialize Models
@st.cache_resource
def load_models():
    pose = mp_pose.Pose(
        static_image_mode=True,
        model_complexity=0,
        min_detection_confidence=0.5
    )
    face_detection = mp_face.FaceDetection(min_detection_confidence=0.6)
    return pose, face_detection

pose_model, face_model = load_models()

def analyze_posture(image_pil, pose, sensitivity_angle=70):
    """Analyze posture from PIL image"""
    image_np = np.array(image_pil)
    results = pose.process(image_np)
    
    status = "✅ Good Posture"
    angle = 0.0
    landmarks_data = None
    
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        ear_lm = landmarks[mp_pose.PoseLandmark.LEFT_EAR.value]
        shoulder_lm = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        
        ear = [ear_lm.x, ear_lm.y]
        shoulder = [shoulder_lm.x, shoulder_lm.y]
        
        radians = np.arctan2(shoulder[1] - ear[1], shoulder[0] - ear[0])
        angle = np.abs(radians * 180.0 / np.pi)
        
        landmarks_data = (ear, shoulder)
        
        if angle < sensitivity_angle or angle > 110:
            status = "⚠️ Slouching Detected!"
        
    return status, angle, landmarks_data

def detect_faces(image_pil, face_detector):
    """Detect faces and intruders"""
    image_np = np.array(image_pil)
    results = face_detector.process(image_np)
    
    face_count = 0
    security_status = "✅ Safe"
    detections = []
    
    if results.detections:
        face_count = len(results.detections)
        
        if face_count > 1:
            security_status = "🚨 INTRUDER DETECTED!"
        else:
            security_status = "✅ Safe (1 Face)"
        
        for detection in results.detections:
            detections.append(detection)
    
    return security_status, face_count, detections

def draw_annotations(image_pil, landmarks_data, detections):
    """Draw posture and face annotations on image"""
    image_copy = image_pil.copy()
    draw = ImageDraw.Draw(image_copy)
    w, h = image_pil.size
    
    # Draw posture line
    if landmarks_data:
        ear, shoulder = landmarks_data
        ear_px = (int(ear[0] * w), int(ear[1] * h))
        shoulder_px = (int(shoulder[0] * w), int(shoulder[1] * h))
        
        draw.line([ear_px, shoulder_px], fill=(0, 255, 0), width=3)
        draw.ellipse([ear_px[0]-6, ear_px[1]-6, ear_px[0]+6, ear_px[1]+6], fill=(0, 255, 0))
        draw.ellipse([shoulder_px[0]-6, shoulder_px[1]-6, shoulder_px[0]+6, shoulder_px[1]+6], fill=(0, 255, 0))
    
    # Draw face detections
    for detection in detections:
        bboxC = detection.location_data.relative_bounding_box
        xmin = int(bboxC.xmin * w)
        ymin = int(bboxC.ymin * h)
        box_width = int(bboxC.width * w)
        box_height = int(bboxC.height * h)
        
        box_color = (0, 255, 0) if len(detections) == 1 else (255, 0, 0)
        
        draw.rectangle([xmin, ymin, xmin + box_width, ymin + box_height], outline=box_color, width=2)
        
        label = "User" if len(detections) == 1 else "INTRUDER!"
        draw.text((xmin, ymin - 10), label, fill=box_color)
    
    return image_copy

# Main Layout
col1, col2 = st.columns([3, 1])

st.subheader("📤 Upload Image to Analyze")
st.write("Upload a photo to analyze posture and detect intruders.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Load image
    image_pil = Image.open(uploaded_file).convert('RGB')
    
    with col1:
        st.subheader("📹 Analysis")
        
        # Analyze posture
        posture_status, angle, landmarks_data = analyze_posture(image_pil, pose_model, sensitivity)
        
        # Detect intruders
        security_status, face_count, detections = detect_faces(image_pil, face_model)
        
        # Draw annotations
        annotated_image = draw_annotations(image_pil, landmarks_data, detections)
        
        st.image(annotated_image, use_column_width=True)
    
    with col2:
        st.subheader("📊 Results")
        st.metric(label="Posture", value=posture_status, delta=f"{angle:.1f}°")
        st.metric(label="Security", value=security_status, delta=f"{face_count} face(s)")
        st.metric(label="Status", value="Analysis Complete")

else:
    with col1:
        st.info("👆 Upload an image to get started!")
    
    with col2:
        st.subheader("📊 Results")
        st.write("Upload an image to see analysis results here")

st.divider()
st.markdown("""
### ℹ️ About This App
- **Posture Detection**: Analyzes head-to-shoulder angle to detect slouching
- **Intruder Detection**: Detects if multiple faces are in frame
- **Privacy Focused**: All processing happens on your device
- **No Data Collection**: Images are never stored or sent anywhere

### 🚀 For Live Monitoring
Run the desktop app locally:
```bash
pip install -r requirements.txt
python main.py
```
""")
