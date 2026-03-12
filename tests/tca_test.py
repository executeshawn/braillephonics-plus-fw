from smbus2 import SMBus
import time

bus = SMBus(1)

TCA_ADDRESSES = [0x70, 0x71]

def select_channel(tca_addr, channel):
    bus.write_byte(tca_addr, 1 << channel)
    time.sleep(0.05)

def scan_bus():
    devices = []
    for addr in range(0x03, 0x78):
        try:
            bus.write_quick(addr)
            devices.append(addr)
        except:
            pass
    return devices

for tca in TCA_ADDRESSES:
    print(f"\nScanning TCA at 0x{tca:02X}")
    for ch in range(8):
        select_channel(tca, ch)
        devices = scan_bus()
        
        # Remove multiplexer addresses
        devices = [d for d in devices if d not in TCA_ADDRESSES]
        
        print(f" Channel {ch}: ", end="")
        if devices:
            for d in devices:
                print(f"0x{d:02X} ", end="")
        else:
            print("No devices")
        print()