import time
import board
import busio
import sqlite3
from smbus2 import SMBus
from adafruit_pn532.i2c import PN532_I2C

# -----------------------------
# TCA9548A configuration
# -----------------------------
TCA1_ADDR = 0x70
CHANNEL = 0  # SD0/SC0

bus = SMBus(1)

def select_tca_channel(tca_addr, channel):
    bus.write_byte(tca_addr, 1 << channel)
    time.sleep(0.1)

# -----------------------------
# DATABASE
# -----------------------------
conn = sqlite3.connect("nfc_tags.db")
cursor = conn.cursor()

def get_letter(uid):
    uid_str = ''.join([format(i, '02X') for i in uid])
    cursor.execute("SELECT symbol FROM nfc_tags WHERE uid=?", (uid_str,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# -----------------------------
# Select TCA channel
# -----------------------------
select_tca_channel(TCA1_ADDR, CHANNEL)

# -----------------------------
# Initialize PN532
# -----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

pn532.SAM_configuration()

print("Waiting for NFC card...")

# -----------------------------
# NFC Reading Loop
# -----------------------------
while True:
    uid = pn532.read_passive_target(timeout=0.05)

    if uid:
        letter = get_letter(uid)

        if letter:
            print("Card detected! Letter:", letter)
        else:
            uid_hex = ''.join([format(i, '02X') for i in uid])
            print("Unknown card detected! UID:", uid_hex)

        time.sleep(1)