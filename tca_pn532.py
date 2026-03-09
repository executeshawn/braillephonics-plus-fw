import time
import board
import busio
from smbus2 import SMBus
from adafruit_pn532.i2c import PN532_I2C

# -----------------------------
# TCA9548A configuration
# -----------------------------
TCA1_ADDR = 0x70
TCA2_ADDR = 0x71
CHANNEL = 0  # SD0/SC0

def select_tca_channel(tca_addr, channel):
    bus = SMBus(1)
    bus.write_byte(tca_addr, 1 << channel)
    bus.close()
    time.sleep(0.2)

# -----------------------------
# Select TCA channel
# -----------------------------
print("Selecting TCA9548A channel...")

select_tca_channel(TCA1_ADDR, CHANNEL)
# If you want to test the second multiplexer:
# select_tca_channel(TCA2_ADDR, CHANNEL)

# -----------------------------
# Initialize PN532
# -----------------------------
print("Initializing PN532...")

i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

ic, ver, rev, support = pn532.firmware_version
print(f"PN532 Firmware: {ver}.{rev}")

pn532.SAM_configuration()


print("Waiting for NFC card...")

# -----------------------------
# Read NFC Card
# -----------------------------
while True:
    uid = pn532.read_passive_target(timeout=0.05)

    if uid:
        print("Card detected:", [hex(i) for i in uid])
        time.sleep(1)
