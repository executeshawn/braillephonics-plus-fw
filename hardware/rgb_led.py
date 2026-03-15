import lgpio
import time

class RGBLed:

    def __init__(self, red=23, green=16, blue=20):

        self.h = lgpio.gpiochip_open(0)

        self.red = red
        self.green = green
        self.blue = blue

        for pin in [red, green, blue]:
            lgpio.gpio_claim_output(self.h, pin)

    def red_on(self):
        lgpio.gpio_write(self.h, self.red, 1)

    def green_on(self):
        lgpio.gpio_write(self.h, self.green, 1)

    def blue_on(self):
        lgpio.gpio_write(self.h, self.blue, 1)

    def off(self):

        for pin in [self.red, self.green, self.blue]:
            lgpio.gpio_write(self.h, pin, 0)