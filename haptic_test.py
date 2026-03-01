import lgpio
import time

HAPTIC_PIN = 26
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, HAPTIC_PIN)

def vibrate(duration):
    lgpio.gpio_write(h, HAPTIC_PIN, 1)
    time.sleep(duration)
    lgpio.gpio_write(h, HAPTIC_PIN, 0)

def success_feedback():
    vibrate(0.2)
    time.sleep(0.1)
    vibrate(0.2)

def error_feedback():
    vibrate(1)

try:
    print("Testing success pattern")
    success_feedback()
    time.sleep(2)

    print("Testing error pattern")
    error_feedback()

finally:
    lgpio.gpio_write(h, HAPTIC_PIN, 0)
    lgpio.gpiochip_close(h)