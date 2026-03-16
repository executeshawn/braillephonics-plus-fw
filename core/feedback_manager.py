# core/feedback_manager.py
import time

class FeedbackManager:
    """
    Handles audio, haptic, and RGB feedback for all three modes:
    - Letter recognition
    - Phonics practice
    - Word formation
    """

    def __init__(self, audio, haptic, rgb):
        self.audio = audio      # instance of AudioAmp
        self.haptic = haptic    # instance of HapticDriver
        self.rgb = rgb          # instance of RGBLed

    # ----------------------------
    # Letter Recognition Mode
    # ----------------------------
    def letter_mode(self, letter):
        self.audio.speak(f"Letter {letter}")
        self.haptic.vibrate(0.2)
        time.sleep(0.1)
        self.haptic.vibrate(0.2)
        self.rgb.green_on()
        time.sleep(1)
        self.rgb.off()

    # ----------------------------
    # Phonics Practice Mode
    # ----------------------------
    def phonics_mode(self, letter):
        self.audio.speak(letter)
        self.haptic.vibrate(0.2)
        self.rgb.green_on()
        time.sleep(1)
        self.rgb.off()

    # ----------------------------
    # Word Formation Mode (per tile)
    # ----------------------------
    def word_mode(self, word, valid=None):
        """
        word: current word or tile string
        valid: optional boolean indicating if the word is valid
        """
        # Speak the current word or tile
        self.audio.speak(word)

        # Provide haptic + RGB feedback if validity is provided
        if valid is not None:
            if valid:
                self.haptic.vibrate(0.2)
                self.rgb.green_on()
                time.sleep(1)
                self.rgb.off()
            else:
                self.haptic.vibrate(1)
                self.rgb.red_on()
                time.sleep(1)
                self.rgb.off()
        else:
            # Default tile feedback if no validity provided
            self.haptic.vibrate(0.2)
            self.rgb.green_on()
            time.sleep(1)
            self.rgb.off()

    # ----------------------------
    # Incorrect tile or unknown tag
    # ----------------------------
    def incorrect(self):
        self.audio.speak("Wrong tile placement")
        self.haptic.vibrate(1)
        self.rgb.red_on()
        time.sleep(1)
        self.rgb.off()

    # ----------------------------
    # Full word feedback (valid/invalid)
    # ----------------------------
    def give_feedback(self, word, valid):
        """
        Gives feedback for a fully formed word
        """
        self.word_mode(word, valid)