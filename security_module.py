# security_module.py - Security Module
# Assigned to: Vanshika

import cv2
import ctypes
import os
import platform
import mediapipe as mp
import mediapipe.python.solutions.face_detection as mp_face

class SecuritySentinel:
    def __init__(self):
        self.mp_face = mp_face
        self.face_detection = self.mp_face.FaceDetection(min_detection_confidence=0.6)

    def detect_intruders(self, frame):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)
        
        face_count = 0
        if results.detections:
            face_count = len(results.detections)
            box_color = (0, 255, 0) if face_count == 1 else (0, 0, 255)

            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                xmin = int(bboxC.xmin * w)
                ymin = int(bboxC.ymin * h)
                box_width = int(bboxC.width * w)
                box_height = int(bboxC.height * h)

                cv2.rectangle(frame, (xmin, ymin), (xmin + box_width, ymin + box_height), box_color, 2)
                
                label = "User" if face_count == 1 else "INTRUDER!"
                cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

        return {"face_count": face_count, "intruder_detected": face_count > 1, "frame": frame}

    def lock_screen(self):
        sys_os = platform.system()
        if sys_os == "Windows":
            ctypes.windll.user32.LockWorkStation()
        elif sys_os == "Darwin":
            os.system("pmset displaysleepnow")
        elif sys_os == "Linux":
            os.system("gnome-screensaver-command -l")