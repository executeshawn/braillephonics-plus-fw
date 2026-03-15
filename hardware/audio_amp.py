import subprocess

class AudioAmp:

    def speak(self, text):

        subprocess.Popen([
            "espeak",
            "-s", "140",
            "-p", "60",
            "-ven+f4",
            text
        ])