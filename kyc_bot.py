import speech_recognition as sr
import pyttsx3
import json
import re
import time
from datetime import datetime
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

import os
from gtts import gTTS
import playsound

class KYCVoiceBot:
    def __init__(self):
        # Initialize pyttsx3 engine as primary
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
        except Exception:
            self.engine = None

        # Initialize Recognizer
        self.recognizer = sr.Recognizer()
        self.use_speech = True
        
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                print(f"{Fore.CYAN}Calibrating microphone for ambient noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print(f"{Fore.GREEN}Ready!")
        except (OSError, AttributeError):
            print(f"{Fore.RED}Microphone not available (PyAudio might be missing). Switching to text input mode.")
            self.use_speech = False

    def speak(self, text):
        """Convert text to speech using gTTS (primary) and pyttsx3 (fallback)."""
        print(f"{Fore.YELLOW}Bot: {text}")
        
        # Method 1: Try gTTS (More reliable on this setup)
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            # Use unique filename to avoid permission issues on Windows
            filename = f"temp_{int(time.time())}_{id(text)}.mp3"
            tts.save(filename)
            playsound.playsound(filename)
            try:
                os.remove(filename) # Clean up
            except PermissionError:
                pass # Ignore if file is locked, Windows cleans temp eventually
            return
        except Exception as e:
            # print(f"gTTS failed: {e}") # Debug only
            pass

        # Method 2: Fallback to pyttsx3
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass 
        
        time.sleep(0.5)

    def listen(self, prompt=None):
        """Listen to user input and return text."""
        if prompt:
            self.speak(prompt)
        
        if not self.use_speech:
            print(f"{Fore.CYAN}Enter your response:")
            return input(f"{Fore.WHITE}User (Text): ").lower()

        with self.microphone as source:
            print(f"{Fore.CYAN}Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                print(f"{Fore.WHITE}User (Speech): {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                print(f"{Fore.RED}Timeout: No speech detected.")
                return None
            except sr.UnknownValueError:
                print(f"{Fore.RED}Could not understand audio.")
                return None
            except sr.RequestError as e:
                print(f"{Fore.RED}Speech Service Error: {e}")
                return None

    def validate_input(self, prompt, validator_func, error_msg, max_retries=2):
        """Generic input collection with validation and retries."""
        attempts = 0
        while attempts <= max_retries:
            response = self.listen(prompt)
            
            if response:
                # Pre-process response (e.g., remove spaces for phone/pan if spoken with pauses)
                cleaned_response = response.replace(" ", "")
                if validator_func(response, cleaned_response):
                    return response, cleaned_response
            
            # If validation fails or no input
            attempts += 1
            if attempts <= max_retries:
                self.speak(f"{error_msg}. Please try again.")
            else:
                self.speak("I'm sorry, I couldn't verify that detail. Let's move on or restart.")
                return None, None
        return None, None

    # Validation Logic
    def is_valid_name(self, original, cleaned):
        return len(original.strip()) > 0

    def is_valid_phone(self, original, cleaned):
        # Check for 10 digits
        # Spoken numbers might be "nine eight..." -> map words to digits if needed?
        # For simplicity, assuming digits are recognized as numbers by Google STT or user says "9 8 7..."
        # Basic check: extract all digits
        digits = "".join(filter(str.isdigit, cleaned))
        return len(digits) == 10

    def is_valid_pan(self, original, cleaned):
        # PAN structure: 5 chars, 4 digits, 1 char (e.g., ABCDE1234F)
        # Speech recognition for alphanumeric codes is tricky ("A as in Apple" etc).
        # We'll validte simple regex on the recognized string.
        # Google STT often outputs "abcde 1234 f"
        # We will try to normalize
        # Removing spaces and forcing upper case
        candidate = cleaned.upper()
        # Basic regex for PAN (simplified for speech which might misinterpret)
        # Requirement: "10 alphanum"
        return len(candidate) == 10 and candidate.isalnum()

    def is_valid_consent(self, original, cleaned):
        return "yes" in original or "agree" in original or "consent" in original

    def start_kyc_process(self):
        session_data = {}
        
        self.speak("Welcome to Decentro KYC verification.")

        # 1. Name
        # Validation: Non-empty
        raw_name, _ = self.validate_input(
            "May I have your full name?",
            self.is_valid_name,
            "I didn't catch a valid name"
        )
        if not raw_name: return # Exit or handle graceful fail
        session_data['name'] = raw_name

        # 2. Phone
        # Validation: 10 digits
        # Note: Spoken numbers can be tricky.
        user_phone, cleaned_phone = self.validate_input(
            "Please provide your 10-digit phone number.",
            self.is_valid_phone,
            "That didn't sound like a 10 digit number"
        )
        if not user_phone: return
        # Extract digits for storage
        session_data['phone'] = "".join(filter(str.isdigit, cleaned_phone))

        # 3. PAN
        # Validation: 10 alphanum
        user_pan, cleaned_pan = self.validate_input(
            "Please state your 10-character PAN number.",
            self.is_valid_pan,
            "Invalid PAN format, it should be 10 alphanumeric characters"
        )
        if not user_pan: return
        session_data['pan'] = cleaned_pan.upper()

        # Summary
        self.speak(f"Confirming details. Name: {session_data['name']}. Phone: {session_data['phone']}. PAN: {session_data['pan']}.")
        
        # 4. Consent
        # Final explicit consent
        # Using a longer phrase "Yes I consent" improves recognition accuracy over just "Yes"
        user_consent, _ = self.validate_input(
            "Do you consent to verification? Please say 'Yes, I consent' or 'No'.",
            self.is_valid_consent,
            "I need a clear confirmation. Please say 'Yes, I consent'."
        )
        
        if user_consent:
            session_data['consent'] = True
            session_data['timestamp'] = datetime.now().isoformat()
            
            # Save JSON
            filename = f"kyc_session_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=4)
            
            self.speak("Thank you. Your details have been recorded. Verification is processing.")
            print(f"\n{Fore.GREEN}Session saved to {filename}")
            print(json.dumps(session_data, indent=4))
        else:
            self.speak("Verification cancelled. Have a nice day.")
            session_data['consent'] = False
            session_data['error'] = "User denied consent or input failed."

if __name__ == "__main__":
    try:
        bot = KYCVoiceBot()
        bot.start_kyc_process()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
