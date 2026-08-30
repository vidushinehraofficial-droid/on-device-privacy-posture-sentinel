# app.py - Live WebRTC Streamlit Web Application
import streamlit as st
import cv2
import av
from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    WebRtcMode,
    RTCConfiguration,
)
from vision_module import PostureTracker
from security_module import SecuritySentinel

st.set_page_config(page_title="Privacy & Posture Sentinel", layout="wide")
st.title("🛡️ On-Device Privacy & Posture Sentinel")

# ---------------------------------------------------------------------------
# WebRTC / ICE configuration — REQUIRED for deployment (Streamlit Cloud, HF
# Spaces, etc). Without this, the browser and server can't find each other
# over the internet, so the camera works locally but not once deployed.
# ---------------------------------------------------------------------------
RTC_CONFIGURATION = RTCConfiguration(
    {
        "iceServers": [
            {"urls": ["stun:stun.l.google.com:19302"]},
        ]
    }
)

# If the camera still won't connect after deploying (common on strict
# office/college wifi), comment out the block above and use this one
# instead, which adds a free TURN relay:
#
# RTC_CONFIGURATION = RTCConfiguration(
#     {
#         "iceServers": [
#             {"urls": "stun:stun.relay.metered.ca:80"},
#             {
#                 "urls": "turn:global.relay.metered.ca:80",
#                 "username": "openrelayproject",
#                 "credential": "openrelayproject",
#             },
#             {
#                 "urls": "turn:global.relay.metered.ca:443",
#                 "username": "openrelayproject",
#                 "credential": "openrelayproject",
#             },
#         ]
#     }
# )

# Sidebar Controls
st.sidebar.header("Controls & Settings")
sensitivity = st.sidebar.slider("Slouch Sensitivity Angle", min_value=60, max_value=85, value=70)


# Initialize AI Modules
@st.cache_resource
def get_sentinels():
    return PostureTracker(), SecuritySentinel()


posture_tracker, security_sentinel = get_sentinels()


# Video Processor Class for WebRTC Browser Stream
class SentinelVideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.sensitivity = 70

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        try:
            # Process frame using Yashika's & Vanshika's modules
            posture_data = posture_tracker.analyze_posture(
                img, sensitivity_angle=self.sensitivity, audio_enabled=False
            )
            security_data = security_sentinel.detect_intruders(posture_data["frame"])
            out_img = security_data["frame"]
        except Exception as e:
            # Don't let a module error kill the whole stream — draw the
            # error on-frame instead so it's visible during a live demo.
            out_img = img
            cv2.putText(
                out_img,
                f"Processing error: {e}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1,
            )

        return av.VideoFrame.from_ndarray(out_img, format="bgr24")


# Launch Live WebRTC Streamer inside browser
ctx = webrtc_streamer(
    key="sentinel-feed",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=SentinelVideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

if ctx.video_processor:
    ctx.video_processor.sensitivity = sensitivity

# ---------------------------------------------------------------------------
# Connection status — helpful for debugging on a deployed demo. Tells you
# whether it's a WebRTC connection issue vs a module/logic issue.
# ---------------------------------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("Connection Status")
st.sidebar.write(f"State: `{ctx.state}`")

if ctx.state.playing:
    st.sidebar.success("Camera connected ✅")
else:
    st.sidebar.warning(
        "Not connected yet. Click **Start**, allow camera access, and wait "
        "a few seconds. If it stays stuck, check browser console (F12) for "
        "ICE errors — you may need the TURN config commented above."
    )