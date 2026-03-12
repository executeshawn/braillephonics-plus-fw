import subprocess
import time

def speak(text):
    """
    Sends text to eSpeak.
    -s 140: Slower speed (default is 175) for better clarity in phonics.
    -p 60: Adjusts pitch (default 50).
    -ven+f4: Uses a female voice variant (optional).
    2>/dev/null: Hides ALSA warnings in the console.
    """
    print(f"Speaking: {text}")
    # Using 'subprocess.Popen' instead of 'os.system' prevents your 
    # NFC scanning loop from freezing while the Pi is talking.
    subprocess.Popen(['espeak', '-s', '140', '-p', '60', '-ven+f4', text, '2>/dev/null'])

# Example usage for your Braillephonics demo
try:
    speak("System ready.")
    time.sleep(2)
    
    # Simulate a tile detection
    detected_letter = "A"
    speak(f"Correct. This is the letter {detected_letter}")
    
except KeyboardInterrupt:
    print("Stopping...")
