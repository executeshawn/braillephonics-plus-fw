import lgpio

class Buttons:

    MODE1 = 4
    MODE2 = 17
    MODE3 = 27

    def __init__(self):

        self.h = lgpio.gpiochip_open(0)

        for pin in [self.MODE1, self.MODE2, self.MODE3]:
            lgpio.gpio_claim_input(self.h, pin)

    def mode1_pressed(self):
        return lgpio.gpio_read(self.h, self.MODE1) == 1

    def mode2_pressed(self):
        return lgpio.gpio_read(self.h, self.MODE2) == 1

    def mode3_pressed(self):
        return lgpio.gpio_read(self.h, self.MODE3) == 1