import streamlit as st
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Privacy & Posture Sentinel", layout="wide")
st.title("🛡️ On-Device Privacy & Posture Sentinel")

st.warning("""
⚠️ **Note:** This is a **demo/preview version** on Streamlit Cloud with basic image upload functionality.

For **full features** (live posture tracking, intruder detection), run the app locally:
```bash
pip install -r requirements.txt
python main.py
```
""")

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.info("""
    **Features:**
    - 📷 Real-time posture monitoring
    - 👤 Intruder detection
    - ⚠️ Slouch alerts
    - 🔒 Privacy-focused
    
    **Deployment Options:**
    - Local: Full features
    - Web: Preview only
    """)
    
    st.divider()
    
    st.subheader("🚀 Quick Start (Local)")
    st.code("""
pip install -r requirements.txt
python main.py
    """, language="bash")

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Image Upload (Demo)")
    uploaded_file = st.file_uploader("Upload an image to preview", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)
    else:
        st.info("Upload an image to see preview")

with col2:
    st.subheader("✨ Features")
    st.markdown("""
    **Live Version (Local):**
    - ✅ Real-time webcam
    - ✅ Pose detection
    - ✅ Intruder alerts
    - ✅ Audio warnings
    
    **Web Version (Demo):**
    - ⚠️ Image upload only
    - ℹ️ Full ML disabled
    """)

st.divider()

st.subheader("🎯 How to Get Full Features")

st.markdown("""
### Option 1: Run Locally (Recommended)
**Best for:**
- Live posture monitoring
- Real-time intruder detection
- Full feature access

**Steps:**
1. Open terminal/PowerShell
2. Navigate to project folder
3. Run these commands:

```bash
pip install -r requirements.txt
python main.py
```

### Option 2: Web Preview (Limited)
- Use this page to explore the UI
- Full ML features only work locally
- Due to Streamlit Cloud limitations

### System Requirements
- Python 3.8+
- Webcam (for local version)
- Windows/Mac/Linux

### Need Help?
Check the `SETUP_GUIDE.md` in the repository for detailed instructions.
""")

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 What This App Does")
    st.markdown("""
    1. **Posture Tracking**
       - Monitors head & shoulder position
       - Detects slouching
       - Real-time alerts
    
    2. **Intruder Detection**
       - Counts faces in view
       - Alerts if >1 person
       - Auto-locks screen option
    """)

with col_b:
    st.subheader("🔐 Privacy & Security")
    st.markdown("""
    - 🛡️ **On-Device Processing**
      All analysis happens locally
    
    - 🚫 **No Cloud Upload**
      Images never sent anywhere
    
    - 👤 **No Tracking**
      No user data collected
    
    - 🔒 **Private**
      Fully encrypted, open-source
    """)

st.divider()
st.caption("Made with ❤️ • Privacy-First • Open Source")
