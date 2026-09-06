# gui_module.py - Integrated GUI with CTkImage
# Assigned to: Person 3

import customtkinter as ctk
import cv2
import time
from PIL import Image, ImageFilter, ImageGrab

class SentinelApp(ctk.CTk):
    def __init__(self, posture_tracker, security_sentinel):
        super().__init__()

        self.title("On-Device Privacy & Posture Sentinel")
        self.geometry("1120x720")
        self.minsize(980, 640)
        self.configure(fg_color="#0B1118")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.posture_tracker = posture_tracker
        self.security_sentinel = security_sentinel
        
        self.start_time = time.time()
        self.total_frames = 0
        self.good_frames = 0

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Video Canvas Container
        self.video_frame = ctk.CTkFrame(self, corner_radius=18, fg_color="#121B25", border_width=1, border_color="#223242")
        self.video_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # CTkLabel for Video Display
        self.video_label = ctk.CTkLabel(self.video_frame, text="Starting camera...", text_color="#91A4B7", font=ctk.CTkFont(size=14))
        self.video_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Sidebar Panel
        self.sidebar = ctk.CTkFrame(self, corner_radius=18, width=300, fg_color="#101821", border_width=1, border_color="#223242")
        self.sidebar.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.sidebar.grid_propagate(False)

        self.title_label = ctk.CTkLabel(self.sidebar, text="SENTINEL", text_color="#F4F7FA", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(22, 0))
        self.subtitle_label = ctk.CTkLabel(self.sidebar, text="Privacy posture monitor", text_color="#7F93A6", font=ctk.CTkFont(size=11))
        self.subtitle_label.pack(pady=(0, 18))

        self.posture_card = ctk.CTkFrame(self.sidebar, fg_color="#17232D", corner_radius=12)
        self.posture_card.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(self.posture_card, text="Posture Status", font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
        self.posture_val = ctk.CTkLabel(self.posture_card, text="Checking...", font=ctk.CTkFont(size=15, weight="bold"))
        self.posture_val.pack(pady=(0, 4))

        self.security_card = ctk.CTkFrame(self.sidebar, fg_color="#17232D", corner_radius=12)
        self.security_card.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(self.security_card, text="Security Sentinel", font=ctk.CTkFont(size=11)).pack(pady=(4, 0))
        self.security_val = ctk.CTkLabel(self.security_card, text="Safe (1 Face)", font=ctk.CTkFont(size=15, weight="bold"))
        self.security_val.pack(pady=(0, 4))

        self.stats_card = ctk.CTkFrame(self.sidebar, fg_color="#17232D", corner_radius=12)
        self.stats_card.pack(fill="x", padx=15, pady=6)
        ctk.CTkLabel(self.stats_card, text="Session Analytics", font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(4, 0))
        self.score_label = ctk.CTkLabel(self.stats_card, text="Score: 100%", font=ctk.CTkFont(size=12))
        self.score_label.pack()
        self.timer_label = ctk.CTkLabel(self.stats_card, text="Active: 0m 0s", font=ctk.CTkFont(size=11))
        self.timer_label.pack(pady=(0, 4))

        self.blur_switch = ctk.CTkSwitch(self.sidebar, text="Privacy Blur", progress_color="#2BB673")
        self.blur_switch.select()
        self.blur_switch.pack(pady=10)

        self.audio_switch = ctk.CTkSwitch(self.sidebar, text="Audio Alerts", progress_color="#2BB673")
        self.audio_switch.select()
        self.audio_switch.pack(pady=5)

        self.background_button = ctk.CTkButton(
            self.sidebar,
            text="Minimize & Monitor",
            command=self.start_background_monitor,
            fg_color="#238B68",
            hover_color="#1D7357",
            height=36,
        )
        self.background_button.pack(fill="x", padx=15, pady=(16, 4))
        self.monitoring_label = ctk.CTkLabel(
            self.sidebar,
            text="Monitoring stays active when minimized",
            text_color="#7F93A6",
            font=ctk.CTkFont(size=10),
        )
        self.monitoring_label.pack(pady=(0, 10))

        self.privacy_overlay = None

        ctk.CTkLabel(self.sidebar, text="Slouch Sensitivity", font=ctk.CTkFont(size=11)).pack(pady=(10, 0))
        self.sensitivity_slider = ctk.CTkSlider(self.sidebar, from_=60, to=85, number_of_steps=25)
        self.sensitivity_slider.set(70)
        self.sensitivity_slider.pack(padx=15, pady=5)

        ctk.CTkLabel(self.sidebar, text="Camera Source", font=ctk.CTkFont(size=11)).pack(pady=(10, 0))
        self.camera_source = ctk.StringVar(value="Auto")
        self.camera_menu = ctk.CTkOptionMenu(
            self.sidebar,
            variable=self.camera_source,
            values=["Auto", "0", "1", "2"],
            command=self.change_camera,
            width=150,
        )
        self.camera_menu.pack(padx=15, pady=5)

        # Open Camera Stream with proper initialization
        self.cap = None
        self.init_camera()
        self.update_feed()

    def change_camera(self, source):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.cap = None
        self.video_label.configure(text=f"Connecting to camera {source}...", image=None)
        self.init_camera()


    def start_background_monitor(self):
        self.title("Sentinel - Monitoring active")
        self.background_button.configure(text="Monitoring in Background")
        self.iconify()

    def show_privacy_overlay(self):
        if self.privacy_overlay is None or not self.privacy_overlay.winfo_exists():
            self.privacy_overlay = ctk.CTkToplevel(self)
            self.privacy_overlay.withdraw()
            self.privacy_overlay.attributes("-topmost", True)

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.privacy_overlay.geometry(f"{screen_width}x{screen_height}+0+0")
            screen_image = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))
            blurred_screen = screen_image.filter(ImageFilter.GaussianBlur(18))
            self.overlay_image = ctk.CTkImage(
                light_image=blurred_screen,
                dark_image=blurred_screen,
                size=(screen_width, screen_height),
            )
            ctk.CTkLabel(self.privacy_overlay, text="", image=self.overlay_image).place(
                relx=0, rely=0, relwidth=1, relheight=1
            )

            ctk.CTkLabel(
                self.privacy_overlay,
                text="PRIVACY SHIELD ACTIVE",
                fg_color="#080D13",
                text_color="#F4F7FA",
                font=ctk.CTkFont(size=30, weight="bold"),
            ).place(relx=0.5, rely=0.46, anchor="center")
            ctk.CTkLabel(
                self.privacy_overlay,
                text="Additional person detected. Display hidden until the workspace is private.",
                fg_color="#080D13",
                text_color="#91A4B7",
                font=ctk.CTkFont(size=14),
            ).place(relx=0.5, rely=0.52, anchor="center")

        self.privacy_overlay.deiconify()
        self.privacy_overlay.lift()

    def hide_privacy_overlay(self):
        if self.privacy_overlay is not None and self.privacy_overlay.winfo_exists():
            self.privacy_overlay.withdraw()
    
    def init_camera(self):
        """Initialize camera - simpler approach"""
        selected_source = self.camera_source.get()
        camera_indices = range(3) if selected_source == "Auto" else [int(selected_source)]
        try:
            camera_backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") else 0
            for camera_index in camera_indices:
                candidate = cv2.VideoCapture(camera_index, camera_backend)
                if not candidate.isOpened():
                    candidate.release()
                    continue
                candidate.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                candidate.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                candidate.set(cv2.CAP_PROP_FPS, 30)
                ret, frame = candidate.read()
                if ret and frame is not None and frame.size > 0:
                    self.cap = candidate
                    print(f"[+] Camera initialized on index {camera_index}")
                    return
                candidate.release()
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

        intruder_detected = security_data.get("intruder_detected", False)
        if intruder_detected:
            self.security_val.configure(text="INTRUDER DETECTED!", text_color="#E74C3C")
            if bool(self.blur_switch.get()):
                self.show_privacy_overlay()
        else:
            faces = security_data.get("face_count", 0)
            self.security_val.configure(text=f"Safe ({faces} Face)", text_color="#2ECC71")
            self.hide_privacy_overlay()

        elapsed_sec = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed_sec, 60)
        score = int((self.good_frames / self.total_frames) * 100) if self.total_frames > 0 else 100

        self.score_label.configure(text=f"Posture Score: {score}%")
        self.timer_label.configure(text=f"Active: {mins}m {secs}s")

        # Convert BGR OpenCV image to PIL Image
        display_frame = security_data["frame"]
        if intruder_detected and bool(self.blur_switch.get()):
            display_frame = cv2.GaussianBlur(display_frame, (41, 41), 0)
            cv2.putText(
                display_frame,
                "PRIVACY BLUR ACTIVE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 165, 255),
                2,
            )

        display_frame = cv2.resize(display_frame, (640, 480))
        rgb_img = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)

        # Store image reference (prevents garbage collection)
        self.ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(640, 480))
        self.video_label.configure(image=self.ctk_img)

        self.after(20, self.update_feed)

    def on_closing(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.privacy_overlay is not None and self.privacy_overlay.winfo_exists():
            self.privacy_overlay.destroy()
        cv2.destroyAllWindows()
        self.destroy()