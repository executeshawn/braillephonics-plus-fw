# core/mode_leds.py

import lgpio

class ModeLEDs:

    MODE1_LED = 5
    MODE2_LED = 6
    MODE3_LED = 13

    def __init__(self):

        self.h = lgpio.gpiochip_open(0)

        for pin in [self.MODE1_LED, self.MODE2_LED, self.MODE3_LED]:
            lgpio.gpio_claim_output(self.h, pin)

    def set_mode(self, mode):

        lgpio.gpio_write(self.h, self.MODE1_LED, 0)
        lgpio.gpio_write(self.h, self.MODE2_LED, 0)
        lgpio.gpio_write(self.h, self.MODE3_LED, 0)

        if mode == 1:
            lgpio.gpio_write(self.h, self.MODE1_LED, 1)

        if mode == 2:
            lgpio.gpio_write(self.h, self.MODE2_LED, 1)

        if mode == 3:
            lgpio.gpio_write(self.h, self.MODE3_LED, 1)