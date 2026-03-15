import board
import busio
import time

from hardware.tca_controller import TCAController
from hardware.pn532_reader import PN532Reader
from hardware.audio_amp import AudioAmp
from hardware.haptic_driver import HapticDriver
from hardware.rgb_led import RGBLed

from services.database import Database
from core.tag_processor import TagProcessor
from core.feedback_manager import FeedbackManager


print("Starting BraillePhonics+")

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

# Main loop
while True:

    for ch, reader in enumerate(readers):

        if reader is None:
            continue

        uid = reader.read_tag()

        if uid:

            symbol = processor.process(uid)

            if symbol:

                print(f"Reader {ch}: {symbol}")
                feedback.correct(symbol)

            else:

                print(f"Reader {ch}: Unknown tag")
                feedback.incorrect()

            time.sleep(1)