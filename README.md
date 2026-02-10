# Decentro KYC Voice Bot Prototype

This is a Python-based command-line voice bot designed for basic KYC verification. It simulates a fintech onboarding call by capturing user details (Name, Phone, PAN) via speech, validating them, and confirming consent.

## Features
- **Voice Interaction**: Uses Text-to-Speech (TTS) for prompts and Speech Recognition for user input.
- **Basic Validation**: Checks for non-empty names, 10-digit phone numbers, and 10-character alphanumeric PANs.
- **Retry Logic**: Handles invalid inputs by re-prompting the user up to 2 times.
- **JSON Logging**: Saves the session data to a local JSON file for backend integration.
- **Fallback Mode**: Automatically switches to text input if microphone is unavailable (common on newer Python versions like 3.13+ where PyAudio wheels are missing).

## Requirements
- Python 3.x
- Microphone
- Internet connection (for Google Speech Recognition API)

## Installation

1. Clone this repository or download the files.
2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: On Windows, if `pyaudio` fails to install, you may need to download the appropriate .whl file for your Python version from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) or ensure you have the Microsoft Visual C++ Build Tools installed.*

## Integration with Decentro
This bot produces a JSON file that can be readily consumed by backend systems. To enhance this, you could integrate with **Decentro's Scanner APIs**:
- **Face Match API**: Compare a captured selfie (if added) with the ID photo.
- **OCR API**: Extract text from an uploaded ID image to auto-fill the details instead of asking the user.
- **Background Checks**: Use the collected PAN and Phone to run real-time background checks using Decentro's KYC APIs.

## Usage

### 🎤 For Full Voice Interaction (Recommended)
You need a Python version compatible with `PyAudio` (Python 3.10, 3.11, or 3.12).
If you have multiple Python versions installed, run:
```bash
py -3.11 kyc_bot.py
# OR
python3.11 kyc_bot.py
```

### ⌨️ For Text-Only Mode (Fallback)
If you are using Python 3.13 or newer (e.g., Python 3.14 Beta), voice features may not work due to library incompatibility. The bot will automatically switch to text mode.
```bash
python kyc_bot.py
```

1. The bot will greet you and ask for your details. Speak clearly into your microphone when prompted.
   - **Name**: Speak your full name.
   - **Phone**: Say your 10-digit phone number (e.g., "9 8 7 6 5 4 3 2 1 0").
   - **PAN**: Say your 10-character PAN (e.g., "A B C D E 1 2 3 4 F").
   - **Consent**: Say "Yes" or "I consent" to verify.

## Demo Recording
Per the assignment requirements, you need to submit a 1-minute demo recording.
1. Use your phone to record your computer screen while running the script.
2. Ensure the audio (both the bot's voice and your responses) is clearly audible.
3. Walk through a full successful flow:
   - Start the script.
   - Answer the prompts for Name, Phone, and PAN.
   - Confirm consent.
   - Show the terminal output and the generated JSON file.
4. Upload the video to a file sharing service (Google Drive, Loom, etc.) and include the link here or in your submission email, or place the video file in this repository if size permits.

## Sample Output (JSON)

An example of the generated `kyc_session_timestamp.json`:

```json
{
    "name": "Jane Doe",
    "phone": "9876543210",
    "pan": "ABCDE1234F",
    "consent": true,
    "timestamp": "2023-10-27T10:30:00.123456"
}
```

## Structure
- `kyc_bot.py`: Main application script.
- `requirements.txt`: List of dependencies.
- `README.md`: This file.

## Troubleshooting
- **Microphone errors**: Ensure your default recording device is set correctly in Windows Sound settings.
- **Recognition errors**: Speak clearly and ensure minimal background noise. The bot uses Google's Speech Recognition API which requires an internet connection.
