import time
import board
import busio
from adafruit_tca9548a import TCA9548A
from adafruit_pn532.i2c import PN532_I2C

# 1. Setup I2C (Assumes 10kHz baudrate is already set in /boot/config.txt)
i2c = busio.I2C(board.SCL, board.SDA)

# 2. Define Multiplexers
tca70 = TCA9548A(i2c, address=0x70)
tca71 = TCA9548A(i2c, address=0x71)

readers = []

def init_readers(tca_device, label):
    for ch in range(8):
        print(f"Scanning {label} Channel {ch}...", end=" ", flush=True)
        try:
            # Create a virtual bus for this channel
            channel_bus = tca_device[ch]
            time.sleep(0.05) # Give the MUX a moment to switch
            
            # Attempt to initialize the PN532
            # We wrap this in a retry because PN532s are notoriously slow to wake up
            new_reader = None
            for attempt in range(3):
                try:
                    new_reader = PN532_I2C(channel_bus, debug=False)
                    break
                except Exception:
                    time.sleep(0.1)
            
            if new_reader:
                new_reader.SAM_configuration()
                readers.append(new_reader)
                print("FOUND!")
            else:
                print("Not found.")
        except Exception as e:
            print(f"Error: {e}")

# Run initialization
init_readers(tca70, "TCA 0x70")
init_readers(tca71, "TCA 0x71")

print(f"\nTotal readers active: {len(readers)}")
