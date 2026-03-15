from adafruit_tca9548a import TCA9548A

class TCAController:

    def __init__(self, i2c, address=0x70):
        self.tca = TCA9548A(i2c, address=address)

    def channel(self, ch):
        return self.tca[ch]