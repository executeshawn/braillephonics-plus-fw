from gpiozero import Button, LED
from signal import pause

b1 = Button(4, pull_up=True)
b2 = Button(17, pull_up=True)
b3 = Button(27, pull_up=True)

led1 = LED(5)
led2 = LED(6)
led3 = LED(13)

def mode1():
    led1.on()
    led2.off()
    led3.off()

def mode2():
    led1.off()
    led2.on()
    led3.off()

def mode3():
    led1.off()
    led2.off()
    led3.on()

b1.when_pressed = mode1
b2.when_pressed = mode2
b3.when_pressed = mode3

pause()