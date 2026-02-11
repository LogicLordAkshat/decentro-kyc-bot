# Decentro KYC Voice Bot

A Python-based voice bot designed for seamless KYC verification. This bot simulates a fintech onboarding call, capturing user details (Name, Phone, PAN) via speech, validating them in real-time, and generating a structured JSON output.

**Now optimized for Python 3.10+ (including 3.13/3.14 Beta) with robust audio fallbacks.**

## 🚀 Features
- **Natural Voice Interaction**: Uses Google Text-to-Speech (`gTTS`) for high-quality prompts, with `pyttsx3` as a reliable offline fallback.
- **Robust Speech Recognition**: Implements `speech_recognition` with a custom **SoundDevice** fallback to handle microphone inputs on systems where `PyAudio` fails (common on newer Python versions).
- **Smart Voice Activity Detection (VAD)**: Custom energy-based VAD for snappy, responsive listening.
- **Data Validation**:
  - **Phone**: Validates 10-digit Indian numbers.
  - **PAN**: Validates 10-character alphanumeric PAN format.
- **Session Logging**: Automatically saves verified details to a timestamped JSON file.

---
## 📱 1-Minute Demo Recording

As part of the submission, please record a quick 1-minute video demo using your phone:

1. **Start Recording**: Open your phone camera.
2. **Capture Screen**: Point it at your computer screen.
3. **Run the Bot**: Type `python kyc_bot.py` and hit Enter.
4. **Perform flow**:
   - Speak your Name.
   - Speak a valid Phone Number.
   - Speak a valid PAN.
   - Say "Yes, I consent".
5. **Show Output**: Briefly zoom in on the terminal showing the "Session saved" message and the JSON output.


https://github.com/user-attachments/assets/32b58b3b-28f5-4d16-83cc-147dda85d81f



## 🛠️ Setup & Run Instructions

### Prerequisites
- Python 3.x installed (Works on 3.10, 3.11, 3.12, 3.13, 3.14)
- A working microphone
- Internet connection (for Google Speech recognition and TTS)

### Step 1: Install Dependencies
Open your terminal in the project folder and run:
```bash
pip install -r requirements.txt
```
*Note: This installs `SpeechRecognition`, `gTTS`, `playsound`, `sounddevice`, `numpy`, etc.*

### Step 2: Run the Bot
Simply execute the script:
```bash
python kyc_bot.py
```

### Step 3: Interaction
1. **Name**: Speak your full name clearly.
2. **Phone**: Dictate your 10-digit number.
3. **PAN**: Read out your PAN/ID alphanumeric code.
4. **Consent**: Confirm with "Yes" or "I consent".

**Note**: If the bot switches to "Text input mode", ensure your microphone is connected and allowed in Windows Privacy settings.

---




---

## 📂 Project Structure
- `kyc_bot.py`: The main logic containing the Voice Bot class and VAD implementation.
- `requirements.txt`: List of python packages required.
- `kyc_session_*.json`: Output files containing the captured user data.

## ⚠️ Troubleshooting
- **Audio Error**: If `playsound` error occurs, ensure you have a media player installed or try running as Administrator.
- **Microphone**: If the bot doesn't hear you, it automatically lowers the silence threshold. Try speaking louder or closer to the mic.
