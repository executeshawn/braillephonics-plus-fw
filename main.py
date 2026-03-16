# main.py
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

# Mode Manager (inject FeedbackManager)
mode_manager = ModeManager(feedback)

# Initialize I2C for multiplexer
i2c = busio.I2C(board.SCL, board.SDA)
tca = TCAController(i2c)

# Database
db = Database()

# Tag processor
processor = TagProcessor(db)

# Initialize NFC readers (8 channels for 1st TCA)
readers = []
for ch in range(8):
    try:
        reader = PN532Reader(tca.channel(ch))
        readers.append(reader)
        print(f"Reader {ch} READY")
    except Exception as e:
        readers.append(None)
        print(f"Reader {ch} FAILED: {e}")

print("System ready")
audio.speak("System ready")
time.sleep(2.5)

# Set initial mode
current_mode = mode_manager.get_mode()
mode_leds.set_mode(current_mode)

if current_mode == 1:
    audio.speak("Kharylle Mode")
elif current_mode == 2:
    audio.speak("Phonics practice mode")
elif current_mode == 3:
    audio.speak("Angeli Mode")

# NFC memory filter (to track last seen UID per reader)
last_seen_uid = [None] * 8

# ----------------------------
# Main loop
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

        # Detect tile removal
        if uid is None:
            last_seen_uid[ch] = None
            continue

        # Detect new tile
        if uid != last_seen_uid[ch]:
            last_seen_uid[ch] = uid

            symbol = processor.process(uid)  # Convert UID to letter

            if symbol:
                print(f"Reader {ch}: {symbol}")

                mode = mode_manager.get_mode()

                if mode in [1, 2]:
                    # Letter or Phonics mode
                    if mode == 1:
                        feedback.letter_mode(symbol)
                    else:
                        feedback.phonics_mode(symbol)

                elif mode == 3:
                    # Word Formation Mode
                    row = ch // 4  # 0 or 1
                    col = ch % 4   # 0-3

                    # Place tile and get current word + validity
                    word, valid = mode_manager.handle_tile_placement(row, col, symbol)

                    # --- NEW UPDATE ---
                    # Speak each tile as the word grows
                    # FeedbackManager already handles audio, haptic, and LED
                    # This ensures kid-friendly pronunciation per tile
                    #mode_manager.feedback.word_mode(word, valid)

                    print(f"Current Word: {word}, Valid: {valid}")

            else:
                print(f"Reader {ch}: Unknown tag")
                feedback.incorrect()

            # Small delay after detection
            time.sleep(0.5)

    # Short loop delay
    time.sleep(0.05)