import lgpio
import time

# =========================
# GPIO Configuration (BCM)
# =========================
HAPTIC = 26
RED = 13
GREEN = 16
BLUE = 20

# =========================
# Setup GPIO
# =========================
h = lgpio.gpiochip_open(0)

for pin in [HAPTIC, RED, GREEN, BLUE]:
    lgpio.gpio_claim_output(h, pin)

# =========================
# Basic Control Functions
# =========================
def set_pin(pin, state):
    lgpio.gpio_write(h, pin, state)

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
# Feedback Patterns
# =========================
def system_power_on():
    set_pin(BLUE, 0)

def correct_feedback():
    vibrate(0.2)
    time.sleep(0.1)
    vibrate(0.2)

    set_pin(GREEN, 1)
    time.sleep(1)
    set_pin(GREEN, 0)

def incorrect_feedback():
    vibrate(1)
    blink(RED, 2)

# =========================
# Test Demo
# =========================
try:
    print("System Power ON")
    system_power_on()

    time.sleep(2)

    print("Correct Feedback")
    correct_feedback()

    time.sleep(2)

    print("Incorrect Feedback")
    incorrect_feedback()

    print("Demo complete. Blue stays ON.")

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    for pin in [HAPTIC, RED, GREEN, BLUE]:
        set_pin(pin, 0)
    lgpio.gpiochip_close(h)
