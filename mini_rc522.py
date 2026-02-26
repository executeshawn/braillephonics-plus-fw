import spidev
import lgpio
import time

# GPIO setup
RST_PIN = 25

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, RST_PIN)

# Set RST HIGH
lgpio.gpio_write(h, RST_PIN, 1)
time.sleep(0.1)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def read_register(reg):
    val = spi.xfer2([(reg << 1) & 0x7E, 0x00])
    return val[1]

try:
    version = read_register(0x37)
    print("MFRC522 Version register:", hex(version))
finally:
    spi.close()
    lgpio.gpiochip_close(h)