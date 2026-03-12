import lgpio
import time
import os

# =========================
# GPIO CONFIG
# =========================
HAPTIC = 24
RED = 23
GREEN = 16
BLUE = 20   # make this separate LED physically if possible

h = lgpio.gpiochip_open(0)

for pin in [HAPTIC, RED, GREEN, BLUE]:
    lgpio.gpio_claim_output(h, pin)

# =========================
# BASIC CONTROL
# =========================
def set_pin(pin, state):
    lgpio.gpio_write(h, pin, state)

def speak(text):
    os.system(f'espeak "{text}"')

def vibrate(duration):
    set_pin(HAPTIC, 1)
    time.sleep(duration)
    set_pin(HAPTIC, 0)

def blink(pin, times, on_time=0.2, off_time=0.2):
    for _ in range(times):
        set_pin(pin, 1)
        time.sleep(on_time)
        set_pin(pin, 0)
        time.sleep(off_time)

# =========================
# FEEDBACK EVENTS
# =========================
def system_power_on():
    set_pin(BLUE, 0)
    speak("System ready")

def correct_feedback():
    speak("Correct. This is letter A.")

    vibrate(0.2)
    time.sleep(0.1)
    vibrate(0.2)

    set_pin(GREEN, 1)
    time.sleep(1)
    set_pin(GREEN, 0)

def incorrect_feedback():
    speak("Wrong tile placement. Try again.")

    vibrate(1)

    blink(RED, 2)

# =========================
# DEMO
# =========================
try:
    system_power_on()
    time.sleep(2)

    correct_feedback()
    time.sleep(3)

    incorrect_feedback()
    time.sleep(3)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    for pin in [HAPTIC, RED, GREEN, BLUE]:
        set_pin(pin, 0)
    lgpio.gpiochip_close(h)
