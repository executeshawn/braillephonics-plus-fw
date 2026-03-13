import time
import board
import busio
import sqlite3
from adafruit_tca9548a import TCA9548A
from adafruit_pn532.i2c import PN532_I2C

# This test validates that the PN532 can read NFC tags and that the UID is correctly mapped to a letter in the database. It assumes you have a table named 'nfc_tags' with columns 'uid' (TEXT) and 'symbol' (TEXT) where you have stored the mappings of UIDs to letters.

# 1. Initialize main I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# 2. Initialize Multiplexer
tca = TCA9548A(i2c, address=0x70)

# 3. Connect to Database
conn = sqlite3.connect("nfc_tags.db")
cursor = conn.cursor()

def get_letter(uid):
    uid_str = ''.join([format(i, '02X') for i in uid])
    cursor.execute("SELECT symbol FROM nfc_tags WHERE uid=?", (uid_str,))
    result = cursor.fetchone()
    return result[0] if result else None # Returns 'A' instead of ('A',)

# 4. Initialize PN532 using the TCA channel
print("Initializing PN532 on Channel 0...")
try:
    # We use tca[0] instead of raw i2c. This handles the switching automatically. change the index if your PN532 is on a different channel.
    pn532 = PN532_I2C(tca[3], debug=False)
    pn532.SAM_configuration()
    print("PN532 Ready!")
except Exception as e:
    print(f"Failed to detect PN532: {e}")
    exit()

print("Waiting for NFC card...")

# 5. Reading Loop
while True:
    print(".", end="", flush=True) # Heartbeat
    uid = pn532.read_passive_target(timeout=0.5)

    if uid:
        letter = get_letter(uid)
        if letter:
            print(f"Card detected! Letter: {letter}")
        else:
            uid_hex = ''.join([format(i, '02X') for i in uid])
            print(f"Unknown card! UID: {uid_hex}")
        
        time.sleep(1) # Delay to prevent double-reads
