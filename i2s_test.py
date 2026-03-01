import numpy as np
import pyaudio
import time

# Audio settings
volume = 0.5
fs = 44100
duration = 3
frequency = 440  # A4 tone

# Generate sine wave
t = np.linspace(0, duration, int(fs * duration), False)
tone = np.sin(frequency * 2 * np.pi * t)
audio = volume * tone

audio = audio.astype(np.float32)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32, 
                channels=1,
                rate=fs,
                output=True)

print("Playing 440Hz test tone...")
stream.write(audio.tobytes())

stream.stop_stream()
stream.close()
p.terminate()

print("Done.")