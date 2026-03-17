# tests/mode_button_led_test.py

from gpiozero import Button
import time

b1 = Button(4, pull_up=True)
b2 = Button(17, pull_up=True)
b3 = Button(27, pull_up=True)

while True:
    print(b1.is_pressed, b2.is_pressed, b3.is_pressed)
    time.sleep(0.2)