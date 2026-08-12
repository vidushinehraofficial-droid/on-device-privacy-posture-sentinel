# Main Application Entry Point
# main.py - Core Application Entry Point

import cv2
from vision_module import PostureTracker
from security_module import SecuritySentinel

def main():
    tracker = PostureTracker()
    sentinel = SecuritySentinel()
    cap = cv2.VideoCapture(0)

    print("[INFO] Starting On-Device Privacy & Posture Sentinel...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run detection pipelines
        posture_data = tracker.process_frame(frame)
        security_data = sentinel.detect_intruders(frame)

        # Check for unauthorized secondary viewers
        if security_data["intruder_detected"]:
            print("[ALERT] Intruder detected! Locking screen...")
            # sentinel.lock_screen() # Uncomment when ready to test live

        cv2.imshow("Sentinel Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
