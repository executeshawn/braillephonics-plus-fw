# tests/tca_pn532_matrix_test.py

import time
import board
import busio
import sqlite3
import adafruit_tca9548a
from adafruit_pn532.i2c import PN532_I2C

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
    return None


# -----------------------------
# I2C + Multiplexer
# -----------------------------
i2c = busio.I2C(board.SCL, board.SDA)

tca1 = adafruit_tca9548a.TCA9548A(i2c, address=0x70)
tca2 = adafruit_tca9548a.TCA9548A(i2c, address=0x71)
# -----------------------------
# Initialize Readers
# -----------------------------
readers = []

print("Initializing PN532 readers...")

for ch in range(16):
    try:
        if ch < 8:
            i2c_channel = tca1[ch]
        else:
            i2c_channel = tca2[ch - 8]

        pn532 = PN532_I2C(i2c_channel, debug=False)
        pn532.SAM_configuration()

        readers.append(pn532)
        print(f"Reader on Channel {ch} READY")

    except Exception as e:
        readers.append(None)
        print(f"Reader on Channel {ch} FAILED: {e}")

print("Initialization complete.")
print("Waiting for NFC cards...\n")
print("Scanning readers...")


# -----------------------------
# SCAN LOOP
# -----------------------------
while True:
    
    print(".", end="", flush=True)

    for ch, reader in enumerate(readers):

        if reader is None:
            continue

        uid = reader.read_passive_target(timeout=0.5)

        if uid:
            
            print(f"Tag detected on Reader {ch}")
            uid_hex = ''.join([format(i, '02X') for i in uid])
            letter = get_letter(uid)

            if letter:
                print(f"[Reader {ch}] Letter detected: {letter}")
            else:
                print(f"[Reader {ch}] Unknown UID: {uid_hex}")

            time.sleep(0.5)

    time.sleep(0.01)