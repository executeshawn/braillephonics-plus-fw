#!/usr/bin/env python3
"""
TCA9548A + PN532 NFC Module v3 Test Script

Hardware setup:
  - TCA9548A #1 at I2C address 0x70
  - TCA9548A #2 at I2C address 0x71
  - PN532 modules connected to SD0/SC0 (channel 0) of each TCA9548A
  - All devices share I2C bus 1 (SDA/SCL on GPIO 2/3)

Usage:
  python3 tca_pn532_test.py
"""

import time
from smbus2 import SMBus, i2c_msg

bus = SMBus(1)

TCA_ADDRESSES  = [0x70, 0x71]
PN532_I2C_ADDR = 0x24

# PN532 commands
CMD_GET_FIRMWARE_VERSION   = 0x02
CMD_INLIST_PASSIVE_TARGET  = 0x4A
BRTY_ISO14443A             = 0x00

# PN532 frame constants
PN532_PREAMBLE    = 0x00
PN532_STARTCODE1  = 0x00
PN532_STARTCODE2  = 0xFF
PN532_POSTAMBLE   = 0x00
PN532_HOST_TO_PN532 = 0xD4
PN532_PN532_TO_HOST = 0xD5


# ---------------------------------------------------------------------------
# TCA9548A helpers
# ---------------------------------------------------------------------------

def tca_select(tca_addr, channel):
    """Enable one channel (0-7) on the given TCA9548A."""
    bus.write_byte(tca_addr, 1 << channel)
    time.sleep(0.05)


def tca_disable_all():
    """Disable all channels on every TCA9548A."""
    for tca in TCA_ADDRESSES:
        try:
            bus.write_byte(tca, 0x00)
        except OSError:
            pass
    time.sleep(0.02)


# ---------------------------------------------------------------------------
# PN532 low-level I2C helpers
# ---------------------------------------------------------------------------

def _checksum(data):
    return (~sum(data) + 1) & 0xFF


def _build_frame(command, params=()):
    """Assemble a PN532 normal information frame."""
    body   = [PN532_HOST_TO_PN532, command] + list(params)
    length = len(body)
    lcs    = (~length + 1) & 0xFF
    dcs    = _checksum(body)
    return bytes([PN532_PREAMBLE, PN532_STARTCODE1, PN532_STARTCODE2,
                  length, lcs] + body + [dcs, PN532_POSTAMBLE])


def _write(frame: bytes) -> bool:
    try:
        msg = i2c_msg.write(PN532_I2C_ADDR, list(frame))
        bus.i2c_rdwr(msg)
        return True
    except OSError:
        return False


def _wait_ready(timeout=1.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            msg = i2c_msg.read(PN532_I2C_ADDR, 1)
            bus.i2c_rdwr(msg)
            if list(msg)[0] & 0x01:   # bit 0 = ready
                return True
        except OSError:
            pass
        time.sleep(0.01)
    return False


def _read(length=32):
    """Read `length` bytes from PN532 (first byte is status, skipped)."""
    try:
        msg = i2c_msg.read(PN532_I2C_ADDR, length + 1)
        bus.i2c_rdwr(msg)
        return list(msg)[1:]   # drop status byte
    except OSError:
        return None


def _find_response(data, response_cmd):
    """Return the payload bytes after D5 <response_cmd>, or None."""
    if data is None:
        return None
    for i in range(len(data) - 1):
        if data[i] == PN532_PN532_TO_HOST and data[i + 1] == response_cmd:
            return data[i + 2:]
    return None


# ---------------------------------------------------------------------------
# PN532 commands
# ---------------------------------------------------------------------------

def pn532_get_firmware_version():
    """
    Returns (IC, Ver, Rev, Support) tuple, or None on failure.
    Response command byte for GetFirmwareVersion is 0x03.
    """
    frame = _build_frame(CMD_GET_FIRMWARE_VERSION)
    if not _write(frame):
        return None
    time.sleep(0.05)
    if not _wait_ready():
        return None
    payload = _find_response(_read(16), 0x03)
    if payload and len(payload) >= 4:
        return tuple(payload[:4])   # IC, Ver, Rev, Support
    return None


def pn532_read_card(timeout=0.5):
    """
    Poll for one ISO14443A card. Returns UID as bytes, or None if no card.
    Response command byte for InListPassiveTarget is 0x4B.
    """
    frame = _build_frame(CMD_INLIST_PASSIVE_TARGET, [0x01, BRTY_ISO14443A])
    if not _write(frame):
        return None
    time.sleep(0.05)
    if not _wait_ready(timeout):
        return None
    payload = _find_response(_read(32), 0x4B)
    if not payload or payload[0] == 0:   # NumTargets == 0
        return None
    # layout after NumTargets: Tg, ATQA(2), SAK(1), NFCIDLen(1), NFCID(n)
    try:
        uid_len = payload[5]
        return bytes(payload[6: 6 + uid_len])
    except IndexError:
        return None


# ---------------------------------------------------------------------------
# Per-channel test
# ---------------------------------------------------------------------------

def test_channel(tca_addr, channel):
    """Select channel, probe PN532, return True if found."""
    tca_disable_all()
    tca_select(tca_addr, channel)

    fw = pn532_get_firmware_version()
    if fw is None:
        print(f"  TCA 0x{tca_addr:02X} ch{channel}: FAIL  PN532 not detected")
        return False

    ic, ver, rev, support = fw
    print(f"  TCA 0x{tca_addr:02X} ch{channel}: OK  PN532 found  "
          f"IC=0x{ic:02X}  FW={ver}.{rev}  Support=0x{support:02X}")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 58)
    print("  TCA9548A + PN532 NFC v3 - Test Script")
    print("=" * 58)

    tca_disable_all()

    # --- Discovery ---
    print("\n[1/2] Scanning for PN532 modules on every TCA channel ...\n")
    active = []
    for tca in TCA_ADDRESSES:
        for ch in range(8):
            if test_channel(tca, ch):
                active.append((tca, ch))
    tca_disable_all()

    if not active:
        print("\n  No PN532 modules found. Check wiring and I2C addresses.")
        bus.close()
        return

    print(f"\n  Found {len(active)} module(s): "
          + ", ".join(f"TCA 0x{t:02X}/ch{c}" for t, c in active))

    # --- Card-scan loop ---
    print("\n[2/2] Card scan loop - place an NFC card near a reader")
    print("      (Ctrl+C to stop)\n")

    try:
        while True:
            for tca_addr, channel in active:
                tca_disable_all()
                tca_select(tca_addr, channel)
                uid = pn532_read_card()
                if uid:
                    uid_str = ":".join(f"{b:02X}" for b in uid)
                    print(f"  TCA 0x{tca_addr:02X} ch{channel} -> Card UID: {uid_str}")
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("\n\n  Stopped by user.")

    finally:
        tca_disable_all()
        bus.close()
        print("  I2C bus closed.")


if __name__ == "__main__":
    main()
