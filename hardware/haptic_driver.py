import lgpio
import time

class HapticDriver:

    def __init__(self, pin=24):

        self.pin = pin
        self.h = lgpio.gpiochip_open(0)

        lgpio.gpio_claim_output(self.h, pin)

    def vibrate(self, duration):

        lgpio.gpio_write(self.h, self.pin, 1)
        time.sleep(duration)
        lgpio.gpio_write(self.h, self.pin, 0)