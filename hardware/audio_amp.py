# core/audio_amp.py

import subprocess

class AudioAmp:

    def speak(self, text):

        subprocess.Popen([
            "espeak",
            "-s", "140",
            "-p", "80",
            "-ven+f4",
            text
        ])