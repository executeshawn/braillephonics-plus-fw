import lgpio
import time

# GPIO number (BCM numbering)
HAPTIC_PIN = 26

# Open GPIO chip (0 is default)
h = lgpio.gpiochip_open(0)

# Claim the pin as output
lgpio.gpio_claim_output(h, HAPTIC_PIN)

print("Starting haptic motor test...")

try:
    while True:
        print("Motor ON")
        lgpio.gpio_write(h, HAPTIC_PIN, 1)  # HIGH
        time.sleep(1)

        print("Motor OFF")
        lgpio.gpio_write(h, HAPTIC_PIN, 0)  # LOW
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping test...")

finally:
    lgpio.gpio_write(h, HAPTIC_PIN, 0)
    lgpio.gpiochip_close(h)