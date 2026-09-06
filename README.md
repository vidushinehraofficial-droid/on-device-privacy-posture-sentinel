# on-device-privacy-posture-sentinel
On-Device Privacy & Posture Sentinel

An on-device computer-vision utility that monitors posture and protects your screen from shoulder surfing. It uses your webcam, OpenCV, and MediaPipe to detect slouching and additional faces without uploading camera frames to a server.

## What It Does

- Detects posture from the user's head and shoulder landmarks.
- Shows `Good Posture` or `Slouching` in the desktop dashboard.
- Plays an optional Windows audio alert when slouching is detected.
- Counts faces visible to the webcam.
- Detects a possible intruder when more than one face is visible.
- Blurs the current primary display behind a full-screen privacy shield when an intruder is detected.
- Continues monitoring while the dashboard is minimized with `Minimize & Monitor`.
- Displays local session statistics, including posture score and active time.

## How It Works

```text
Webcam frame
	|
	+--> MediaPipe Pose --> posture angle --> Good Posture / Slouching
	|
	+--> MediaPipe Face Detection --> face count --> Safe / Intruder
												   |
												   +--> local privacy shield
```

All camera processing happens locally in the Python process. The project does not save recordings or send frames to a cloud service.

## Requirements

- Windows, macOS, or Linux desktop
- Python 3.11 recommended
- A working webcam
- Camera permission for Python or your terminal
- A display that supports the desktop GUI

Python 3.11 is recommended because the project's MediaPipe setup is pinned around that runtime.

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/vidushinehraofficial-droid/on-device-privacy-posture-sentinel.git
cd on-device-privacy-posture-sentinel

py -3.11 -m venv sentinel_env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\sentinel_env\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS/Linux

```bash
git clone https://github.com/vidushinehraofficial-droid/on-device-privacy-posture-sentinel.git
cd on-device-privacy-posture-sentinel

python3.11 -m venv sentinel_env
source sentinel_env/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Desktop Monitor

The desktop monitor is the recommended version for the full workflow. It can continue monitoring while you work in another application.

```powershell
# Windows
& .\sentinel_env\Scripts\Activate.ps1
python main.py
```

```bash
# macOS/Linux
source sentinel_env/bin/activate
python main.py
```

When the dashboard opens:

1. Allow camera access if prompted.
2. Keep one face visible for normal monitoring.
3. Use the `Minimize & Monitor` button to work in another app.
4. The posture and face-detection loop continues while the dashboard is minimized.
5. Restore the dashboard from the taskbar or dock when needed.

## Dashboard Controls

- **Privacy Blur**: enables the full-screen privacy shield when more than one face is detected.
- **Audio Alerts**: enables a periodic Windows beep for slouching.
- **Slouch Sensitivity**: adjusts the posture angle threshold.
- **Minimize & Monitor**: hides the dashboard while keeping webcam processing active.

The privacy shield covers the primary display with a locally generated blurred snapshot. It does not lock the operating system and it does not terminate the current application.

## Deploy the Browser Preview

`streamlit_app.py` provides a browser-based WebRTC view. It is useful for a local preview, but it cannot protect other desktop applications because browser pages cannot place a full-screen overlay over the operating system.

### Run Locally

```bash
python -m pip install -r requirements-cloud.txt
& .\sentinel_env\Scripts\Activate.ps1
python -m streamlit run streamlit_app.py
```

Use `python main.py` when you need monitoring while working in Word, Chrome, VS Code, or another desktop application.

### Streamlit Community Cloud

1. Push the repository to GitHub.
2. Open [share.streamlit.io](https://share.streamlit.io) and choose **New app**.
3. Select this repository and the `main` branch.
4. Set the main file to `streamlit_app.py`.
5. In advanced settings, select Python `3.11` if available.
6. Deploy the app.

The cloud deployment uses `requirements-cloud.txt`. Browser camera permission must be granted when the app opens. This hosted version processes the browser camera stream for the web preview; it cannot blur or hide other applications on the user's laptop.

## Project Structure

```text
.
|-- main.py              # Desktop application entry point
|-- gui_module.py        # CustomTkinter dashboard and privacy shield
|-- vision_module.py     # Posture landmark analysis and audio alerts
|-- security_module.py   # Face counting and intruder detection
|-- streamlit_app.py     # Optional browser/WebRTC preview
|-- test_camera.py       # Webcam diagnostic script
|-- requirements.txt     # Desktop and local dependencies
|-- requirements-cloud.txt
|-- runtime.txt          # Recommended Python runtime
```

## Troubleshooting

### Camera opens but frames fail

Close Camera, Zoom, Teams, Discord, or any other application using the webcam, then run:

```powershell
& .\sentinel_env\Scripts\Activate.ps1
python test_camera.py
```

The test checks camera indexes `0` through `2`. Also check Windows **Settings > Privacy & security > Camera** and allow desktop applications to access the camera.

### The app appears frozen after an intruder is detected

The privacy shield intentionally covers the primary display to hide sensitive work. Remove the additional face from the camera view; the shield should disappear when one face or no face remains. The monitoring process continues in the background.

### No audio alert

Audio alerts are Windows-specific in the current implementation. Confirm that `Audio Alerts` is enabled and that system volume is available.

### Running `security_module.py` directly fails or does nothing

That file defines a module, not an application entry point. Always start the complete desktop application with:

```bash
python main.py
```

## Privacy Notes

- Camera frames are processed in memory on the local device.
- No cloud account or API key is required for desktop monitoring.
- No camera recordings are written by the application.
- Face detection is used for counting visible faces, not for identifying people.
- The privacy shield currently covers the primary display; multi-monitor protection is not implemented.

## License

See [LICENSE](LICENSE).
