# main.py - Complete 3-Person Team Integration
from vision_module import PostureTracker       # Person 1 (Yashika)
from security_module import SecuritySentinel    # Person 2 (Vanshika)
from gui_module import SentinelApp              # Person 3

def main():
    print("[1/3] Initializing Vision Module (Yashika)...")
    posture_tracker = PostureTracker()

    print("[2/3] Initializing Security Sentinel (Vanshika)...")
    security_sentinel = SecuritySentinel()

    print("[3/3] Launching Dashboard Interface (Person 3)...")
    app = SentinelApp(posture_tracker, security_sentinel)
    
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()