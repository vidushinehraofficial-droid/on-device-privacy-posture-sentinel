# 🚀 Web App Deployment Guide (Streamlit Cloud)

## ⚠️ Important Note
**Streamlit Cloud = Preview/Demo Only**

For **live posture monitoring with full features**, run locally:
```bash
pip install -r requirements.txt
python main.py
```

Streamlit Cloud has system library limitations, so the web version is a simplified preview.

---

## Step 1: Create a Streamlit Account

1. Go to **https://share.streamlit.io**
2. Click **Sign up**
3. Use your GitHub account (easiest)
4. Authorize Streamlit to connect

---

## Step 2: Make Repository Public

1. Go to your GitHub repo: `https://github.com/vidushinehraofficial-droid/on-device-privacy-posture-sentinel`
2. Click **Settings** → **General**
3. Set **Visibility** to **Public**
4. Save

---

## Step 3: Deploy to Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **Create app**
3. Fill in the form:
   - **GitHub repo**: `vidushinehraofficial-droid/on-device-privacy-posture-sentinel`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   
4. ⚠️ **IMPORTANT**: Click **Advanced settings**
   - Change **Python requirements file** from `requirements.txt` → `requirements-cloud.txt`
   
5. Click **Deploy**

**Wait 2-3 minutes for deployment...**

---

## Step 4: Share the Link

Once deployed, you'll get a URL like:
```
https://privacy-posture-sentinel-xxx.streamlit.app
```

Share this with your friends! ✅

---

## What Each Version Does

### 🌐 Web Version (Streamlit Cloud)
- ✅ Image upload & preview
- ✅ Browse features
- ❌ No AI/ML processing (system limitations)
- ✅ Mobile friendly

### 💻 Local Version (Desktop)
- ✅ Live webcam monitoring
- ✅ Real-time posture detection
- ✅ Intruder alerts
- ✅ Audio warnings
- ✅ Auto screen lock
- ✅ Full features

---

## Setup Local Version (For Friends)

```bash
# Clone & setup
git clone https://github.com/vidushinehraofficial-droid/on-device-privacy-posture-sentinel.git
cd on-device-privacy-posture-sentinel

# Create virtual environment
python -m venv sentinel_env
.\sentinel_env\Scripts\Activate.ps1  # Windows
# source sentinel_env/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

---

## Troubleshooting

**"Deployment shows error"**
- Make sure you selected `requirements-cloud.txt` in Advanced settings
- Check app logs on Streamlit Cloud dashboard

**"Web app won't load"**
- This is normal - web version is preview only
- For full features, use local version (instructions above)

**"Local app won't run"**
- Make sure virtual environment is activated
- Check Python version is 3.8+
- Ensure webcam is connected

---

## Updating the App

### Local Changes
1. Edit `main.py` or `gui_module.py`
2. Test locally: `python main.py`
3. Commit & push to GitHub
4. Streamlit Cloud auto-redeployes in 1-2 minutes

### Sharing Updates
- Teammates pull latest from GitHub: `git pull`
- No manual redeploy needed!

---

## Project Files

- `main.py` - Main application
- `gui_module.py` - Desktop GUI interface
- `vision_module.py` - Posture tracking
- `security_module.py` - Intruder detection
- `streamlit_app.py` - Web preview
- `requirements.txt` - Local dependencies
- `requirements-cloud.txt` - Streamlit Cloud dependencies

---

**Questions? Check the README.md for more info!**
