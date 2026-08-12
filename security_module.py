# Security & Screen Lock Module - Vanshika
# security_module.py - Security & Screen Lock Module
# Assigned to: Vanshika

import cv2
import mediapipe as mp
import ctypes
import os
import platform

class SecuritySentinel:
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.6)

    def detect_intruders(self, frame):
        """Counts background faces in frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        face_count = 0
        if results.detections:
            face_count = len(results.detections)
            
        return {"face_count": face_count, "intruder_detected": face_count > 1}

    def lock_screen(self):
        """Triggers OS-level screen lock."""
        sys_os = platform.system()
        if sys_os == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif sys_os == "Darwin":  # macOS
            os.system("pmset displaysleepnow")
        elif sys_os == "Linux":
            os.system("gnome-screensaver-command -l")
