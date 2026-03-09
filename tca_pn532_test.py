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
TCA2_ADDR = 0x71
CHANNEL = 0

bus = SMBus(1)

def select_tca_channel(tca_addr, channel):
    bus.write_byte(tca_addr, 1 << channel)
    time.sleep(0.1)

# -----------------------------
# DATABASE INITIALIZATION
# -----------------------------
conn = sqlite3.connect("nfc_tags.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS nfc_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    label TEXT,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# -----------------------------
# SAVE UID FUNCTION
# -----------------------------
def save_uid(uid):

    uid_str = ''.join([format(i, '02X') for i in uid])

    cursor.execute(
        "INSERT OR IGNORE INTO nfc_tags (uid) VALUES (?)",
        (uid_str,)
    )

    conn.commit()

    print("Saved UID:", uid_str)

# -----------------------------
# Select TCA channel
# -----------------------------
print("Selecting TCA9548A channel...")

select_tca_channel(TCA1_ADDR, CHANNEL)

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
# NFC READING LOOP
# -----------------------------
while True:

    uid = pn532.read_passive_target(timeout=0.05)

    if uid:

        uid_hex = ''.join([format(i, '02X') for i in uid])

        print("Card detected:", uid_hex)

        save_uid(uid)

        time.sleep(1)