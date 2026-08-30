# Setup Guide for Collaborators

This project integrates 3 modules for the On-Device Privacy Posture Sentinel:
- **vision_module.py** - Vision/Posture tracking
- **security_module.py** - Security features  
- **gui_module.py** - Dashboard interface

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/vidushinehraofficial-droid/on-device-privacy-posture-sentinel.git
cd on-device-privacy-posture-sentinel
```

### 2. Create Virtual Environment
```bash
# Windows (PowerShell)
python -m venv sentinel_env
.\sentinel_env\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv sentinel_env
source sentinel_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

## Requirements
- Python 3.8+
- OpenCV
- MediaPipe
- NumPy
- CustomTkinter (for GUI)
- Plyer

## Notes
- Make sure your camera is connected and enabled
- The GUI dashboard will launch once all modules initialize successfully
- Press the close button to properly shutdown the application

## For Developers
- Make changes and commit to your branch
- Push changes to GitHub
- All 3 modules work together in `main.py`
