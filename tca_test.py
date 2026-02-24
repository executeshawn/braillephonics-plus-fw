from smbus2 import SMBus
import time

TCA_ADDRESS = 0x70

bus = SMBus(1)

def select_channel(channel):
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be 0-7")

    bus.write_byte(TCA_ADDRESS, 1 << channel)
    print(f"Channel {channel} selected")
    time.sleep(0.1)

def scan_bus():
    print("Scanning I2C bus...")
    for address in range(0x03, 0x77):
        try:
            bus.write_quick(address)
            print(f"Device found at 0x{address:02X}")
        except:
            pass

# MAIN TEST
for ch in range(8):
    select_channel(ch)
    scan_bus()
    print("-" * 30)

bus.close()

