# gui_module.py - Integrated GUI with CTkImage
# Assigned to: Person 3

import customtkinter as ctk
import cv2
import time
from PIL import Image

class SentinelApp(ctk.CTk):
    def __init__(self, posture_tracker, security_sentinel):
        super().__init__()

        self.title("On-Device Privacy & Posture Sentinel")
        self.geometry("1000x680")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.posture_tracker = posture_tracker
        self.security_sentinel = security_sentinel
        
        self.start_time = time.time()
        self.total_frames = 0
        self.good_frames = 0

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Video Canvas Container
        self.video_frame = ctk.CTkFrame(self, corner_radius=15)
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # CTkLabel for Video Display
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Sidebar Panel
        self.sidebar = ctk.CTkFrame(self, corner_radius=15)
        self.sidebar.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.sidebar, text="SENTINEL DASHBOARD", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.pack(pady=(15, 15))

        self.posture_card = ctk.CTkFrame(self.sidebar)
        self.posture_card.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(self.posture_card, text="Posture Status", font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
        self.posture_val = ctk.CTkLabel(self.posture_card, text="Checking...", font=ctk.CTkFont(size=15, weight="bold"))
        self.posture_val.pack(pady=(0, 4))

        self.security_card = ctk.CTkFrame(self.sidebar)
        self.security_card.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(self.security_card, text="Security Sentinel", font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
        self.security_val = ctk.CTkLabel(self.security_card, text="Safe (1 Face)", font=ctk.CTkFont(size=15, weight="bold"))
        self.security_val.pack(pady=(0, 4))

        self.stats_card = ctk.CTkFrame(self.sidebar)
        self.stats_card.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(self.stats_card, text="Session Analytics", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(4, 0))
        self.score_label = ctk.CTkLabel(self.stats_card, text="Score: 100%", font=ctk.CTkFont(size=12))
        self.score_label.pack()
        self.timer_label = ctk.CTkLabel(self.stats_card, text="Active: 0m 0s", font=ctk.CTkFont(size=11))
        self.timer_label.pack(pady=(0, 4))

        self.lock_switch = ctk.CTkSwitch(self.sidebar, text="Auto Screen Lock")
        self.lock_switch.select()
        self.lock_switch.pack(pady=10)

        self.audio_switch = ctk.CTkSwitch(self.sidebar, text="Audio Alerts")
        self.audio_switch.select()
        self.audio_switch.pack(pady=5)

        ctk.CTkLabel(self.sidebar, text="Slouch Sensitivity", font=ctk.CTkFont(size=11)).pack(pady=(10, 0))
        self.sensitivity_slider = ctk.CTkSlider(self.sidebar, from_=60, to=85, number_of_steps=25)
        self.sensitivity_slider.set(70)
        self.sensitivity_slider.pack(padx=15, pady=5)

        # Open Camera Stream with proper initialization
        self.cap = None
        self.init_camera()
        self.update_feed()
    
    def init_camera(self):
        """Initialize camera - simpler approach"""
        # Try camera index 0 with default backend
        try:
            self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                self.cap.set(cv2.CAP_PROP_FPS, 30)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Single buffer
                print(f"[+] Camera initialized on index 0")
                
                # Warm up camera by reading a few frames
                import time
                for i in range(5):
                    ret, frame = self.cap.read()
                    time.sleep(0.1)
                
                return
        except Exception as e:
            print(f"[!] Camera initialization error: {e}")
        
        self.cap = None

    def update_feed(self):
        # If camera not initialized, try to initialize
        if self.cap is None:
            self.init_camera()
            self.video_label.configure(text="Camera connecting...", text_color="#FFA500")
            self.after(500, self.update_feed)
            return
        
        ret, frame = self.cap.read()
        
        if not ret or frame is None or frame.size == 0:
            # Try to reconnect camera
            print("[!] Camera frame read failed, attempting reconnection...")
            if self.cap.isOpened():
                self.cap.release()
            self.cap = None
            self.video_label.configure(text="Camera disconnected\nReconnecting...", text_color="#E74C3C")
            self.after(1000, self.update_feed)
            return
        
        self.total_frames += 1
        sensitivity = int(self.sensitivity_slider.get())
        audio_on = bool(self.audio_switch.get())

        posture_data = self.posture_tracker.analyze_posture(frame, sensitivity_angle=sensitivity, audio_enabled=audio_on)
        security_data = self.security_sentinel.detect_intruders(posture_data["frame"])

        p_status = posture_data.get("status", "Good")
        if p_status == "Good":
            self.good_frames += 1
            self.posture_val.configure(text="Good Posture", text_color="#2ECC71")
        else:
            self.posture_val.configure(text="Slouching!", text_color="#E74C3C")

        if security_data.get("intruder_detected", False):
            self.security_val.configure(text="INTRUDER DETECTED!", text_color="#E74C3C")
            if bool(self.lock_switch.get()):
                self.security_sentinel.lock_screen()
        else:
            faces = security_data.get("face_count", 0)
            self.security_val.configure(text=f"Safe ({faces} Face)", text_color="#2ECC71")

        elapsed_sec = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed_sec, 60)
        score = int((self.good_frames / self.total_frames) * 100) if self.total_frames > 0 else 100

        self.score_label.configure(text=f"Posture Score: {score}%")
        self.timer_label.configure(text=f"Active: {mins}m {secs}s")

        # Convert BGR OpenCV image to PIL Image
        display_frame = cv2.resize(security_data["frame"], (640, 480))
        rgb_img = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)

        # Store image reference (prevents garbage collection)
        self.ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(640, 480))
        self.video_label.configure(image=self.ctk_img)

        self.after(20, self.update_feed)

    def on_closing(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.destroy()