import time

class FeedbackManager:

    def __init__(self, audio, haptic, rgb):

        self.audio = audio
        self.haptic = haptic
        self.rgb = rgb


    def letter_mode(self, letter):

        self.audio.speak(f"Letter {letter}")

        self.haptic.vibrate(0.2)
        time.sleep(0.1)
        self.haptic.vibrate(0.2)

        self.rgb.green_on()
        time.sleep(1)
        self.rgb.off()


    def phonics_mode(self, letter):

        self.audio.speak(letter)

        self.haptic.vibrate(0.2)

        self.rgb.green_on()
        time.sleep(1)
        self.rgb.off()


    def word_mode(self, letter):

        self.audio.speak(f"Tile {letter}")

        self.haptic.vibrate(0.2)

        self.rgb.green_on()
        time.sleep(1)
        self.rgb.off()


    def incorrect(self):

        self.audio.speak("Wrong tile placement")

        self.haptic.vibrate(1)

        self.rgb.red_on()
        time.sleep(1)
        self.rgb.off()