import board
import busio
import time

from hardware.buttons import Buttons
from hardware.mode_leds import ModeLEDs
from core.mode_manager import ModeManager
from hardware.tca_controller import TCAController
from hardware.pn532_reader import PN532Reader
from hardware.audio_amp import AudioAmp
from hardware.haptic_driver import HapticDriver
from hardware.rgb_led import RGBLed

from services.database import Database
from core.tag_processor import TagProcessor
from core.feedback_manager import FeedbackManager


print("Starting BraillePhonics+")

buttons = Buttons()
mode_leds = ModeLEDs()
mode_manager = ModeManager()

mode_leds.set_mode(1)

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Multiplexer
tca = TCAController(i2c)

# Database
db = Database()

# Hardware
audio = AudioAmp()
haptic = HapticDriver()
rgb = RGBLed()

# Core
processor = TagProcessor(db)
feedback = FeedbackManager(audio, haptic, rgb)

# Initialize NFC readers
readers = []

for ch in range(8):

    try:

        reader = PN532Reader(tca.channel(ch))
        readers.append(reader)

        print(f"Reader {ch} READY")

    except:

        readers.append(None)
        print(f"Reader {ch} FAILED")


print("System ready")
audio.speak("System ready")

time.sleep(1.5)

current_mode = mode_manager.get_mode()

if current_mode == 1:
    audio.speak("Letter recognition mode")

elif current_mode == 2:
    audio.speak("Phonics practice mode")

elif current_mode == 3:
    audio.speak("Word formation mode")

last_mode = mode_manager.get_mode()

# Main loop
while True:

    # -------- MODE BUTTONS --------
    if buttons.mode1_pressed() and last_mode != 1:
        mode_manager.set_mode(1)
        mode_leds.set_mode(1)
        audio.speak("Letter recognition mode")
        last_mode = 1

    if buttons.mode2_pressed() and last_mode != 2:
        mode_manager.set_mode(2)
        mode_leds.set_mode(2)
        audio.speak("Phonics practice mode")
        last_mode = 2

    if buttons.mode3_pressed() and last_mode != 3:
        mode_manager.set_mode(3)
        mode_leds.set_mode(3)
        audio.speak("Word formation mode")
        last_mode = 3

    # -------- NFC SCANNING --------
    for ch, reader in enumerate(readers):

        if reader is None:
            continue

        uid = reader.read_tag()

        if uid:

            symbol = processor.process(uid)

            if symbol:

                print(f"Reader {ch}: {symbol}")

                mode = mode_manager.get_mode()

                if mode == 1:
                    feedback.letter_mode(symbol)

                elif mode == 2:
                    feedback.phonics_mode(symbol)

                elif mode == 3:
                    feedback.word_mode(symbol)

            else:

                print(f"Reader {ch}: Unknown tag")
                feedback.incorrect()

            time.sleep(1)