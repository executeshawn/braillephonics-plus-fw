import board
import busio
import time

from hardware.buttons import Buttons
from hardware.mode_leds import ModeLEDs
from core.mode_manager import ModeManager
from core.word_checker import WordChecker
from hardware.tca_controller import TCAController
from hardware.pn532_reader import PN532Reader
from hardware.audio_amp import AudioAmp
from hardware.haptic_driver import HapticDriver
from hardware.rgb_led import RGBLed
from services.database import Database
from core.tag_processor import TagProcessor
from core.feedback_manager import FeedbackManager

print("Starting BraillePhonics+")

# ----------------------------
# Initialize hardware & core
# ----------------------------
buttons = Buttons()
mode_leds = ModeLEDs()

# Audio / Haptic / RGB
audio = AudioAmp()
haptic = HapticDriver()
rgb = RGBLed()

feedback = FeedbackManager(audio, haptic, rgb)

# Mode Manager
mode_manager = ModeManager(feedback)

# ----------------------------
# I2C + TCA (UPDATED FOR 16)
# ----------------------------
i2c = busio.I2C(board.SCL, board.SDA)

# Two multiplexers (IMPORTANT: different addresses)
tca1 = TCAController(i2c, address=0x70)  # Default
tca2 = TCAController(i2c, address=0x71)  # A0 = HIGH

# ----------------------------
# Database + Processing
# ----------------------------
db = Database()
processor = TagProcessor(db)

# ----------------------------
# Initialize 16 NFC Readers
# ----------------------------
readers = []

for ch in range(16):
    try:
        if ch < 8:
            reader = PN532Reader(tca1.channel(ch))
        else:
            reader = PN532Reader(tca2.channel(ch - 8))

        readers.append(reader)
        print(f"Reader {ch} READY")

    except Exception as e:
        readers.append(None)
        print(f"Reader {ch} FAILED: {e}")

print("System ready")
audio.speak("System ready")
time.sleep(2.5)

# ----------------------------
# Initial Mode Setup
# ----------------------------
current_mode = mode_manager.get_mode()
mode_leds.set_mode(current_mode)

if current_mode == 1:
    audio.speak("Kharylle Mode")
elif current_mode == 2:
    audio.speak("Phonics practice mode")
elif current_mode == 3:
    audio.speak("Angeli Mode")

# ----------------------------
# NFC Memory Tracking (UPDATED)
# ----------------------------
last_seen_uid = [None] * 16

# ----------------------------
# Main Loop
# ----------------------------
last_mode = current_mode

while True:

    # -------- MODE BUTTONS --------
    if buttons.mode1_pressed() and last_mode != 1:
        mode_manager.set_mode(1)
        mode_leds.set_mode(1)
        audio.speak("Letter recognition mode")
        last_mode = 1
        time.sleep(0.3)

    elif buttons.mode2_pressed() and last_mode != 2:
        mode_manager.set_mode(2)
        mode_leds.set_mode(2)
        audio.speak("Phonics practice mode")
        last_mode = 2
        time.sleep(0.3)

    elif buttons.mode3_pressed() and last_mode != 3:
        mode_manager.set_mode(3)
        mode_leds.set_mode(3)
        audio.speak("Angeli Mode")
        last_mode = 3
        time.sleep(0.3)

    # -------- NFC SCANNING --------
    for ch, reader in enumerate(readers):

        if reader is None:
            continue

        uid = reader.read_tag()

        # Tile removed
        if uid is None:
            last_seen_uid[ch] = None
            continue

        # New tile detected
        if uid != last_seen_uid[ch]:
            last_seen_uid[ch] = uid

            symbol = processor.process(uid)

            if symbol:
                print(f"Reader {ch}: {symbol}")

                mode = mode_manager.get_mode()

                # ----------------------------
                # MODE 1 & 2
                # ----------------------------
                if mode in [1, 2]:

                    if mode == 1:
                        feedback.letter_mode(symbol)
                    else:
                        feedback.phonics_mode(symbol)

                # ----------------------------
                # MODE 3 (4x4 GRID)
                # ----------------------------
                elif mode == 3:

                    row = ch // 4   # 0–3
                    col = ch % 4    # 0–3

                    word, valid = mode_manager.handle_tile_placement(
                        row, col, symbol
                    )

                    print(f"Current Word: {word}, Valid: {valid}")

            else:
                print(f"Reader {ch}: Unknown tag")
                feedback.incorrect()

            # Debounce delay
            time.sleep(0.5)

    # Loop delay
    time.sleep(0.05)