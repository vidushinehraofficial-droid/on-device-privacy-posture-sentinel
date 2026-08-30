# vision_module.py - Posture Tracking Module
# Assigned to: Yashika

import cv2
import numpy as np
import mediapipe as mp
import mediapipe.python.solutions.pose as mp_pose
import winsound
import time

class PostureTracker:
    def __init__(self):
        self.mp_pose = mp_pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=0, # Lower complexity for faster rendering inside GUI
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.last_beep_time = 0

    def analyze_posture(self, frame, sensitivity_angle=70, audio_enabled=True):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        status = "Good"
        angle = 0.0

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            ear_lm = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR.value]
            shoulder_lm = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]

            ear = [ear_lm.x, ear_lm.y]
            shoulder = [shoulder_lm.x, shoulder_lm.y]

            ear_px = (int(ear[0] * w), int(ear[1] * h))
            shoulder_px = (int(shoulder[0] * w), int(shoulder[1] * h))

            radians = np.arctan2(shoulder[1] - ear[1], shoulder[0] - ear[0])
            angle = np.abs(radians * 180.0 / np.pi)

            if angle < sensitivity_angle or angle > 110:
                status = "Slouching"
                line_color = (0, 0, 255)
                
                if audio_enabled and (time.time() - self.last_beep_time > 3):
                    winsound.Beep(1000, 200)
                    self.last_beep_time = time.time()
            else:
                line_color = (0, 255, 0)

            # Manual OpenCV drawing directly on frame
            cv2.line(frame, ear_px, shoulder_px, line_color, 3)
            cv2.circle(frame, ear_px, 6, line_color, -1)
            cv2.circle(frame, shoulder_px, 6, line_color, -1)

        return {"status": status, "angle": angle, "frame": frame}