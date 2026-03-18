# core/buttons.py

import gpiozero

class Buttons:

    def __init__(self):

        self.mode1 = gpiozero.Button(4, pull_up=True, bounce_time=0.2)
        self.mode2 = gpiozero.Button(17, pull_up=True, bounce_time=0.2)
        self.mode3 = gpiozero.Button(27, pull_up=True, bounce_time=0.2)

    def mode1_pressed(self):
        return self.mode1.is_pressed

    def mode2_pressed(self):
        return self.mode2.is_pressed

    def mode3_pressed(self):
        return self.mode3.is_pressed