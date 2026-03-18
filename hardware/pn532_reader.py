# core/pn532_reader.py

from adafruit_pn532.i2c import PN532_I2C

class PN532Reader:

    def __init__(self, i2c_channel):
        self.reader = PN532_I2C(i2c_channel, debug=False)
        self.reader.SAM_configuration()

    def read_tag(self):
        return self.reader.read_passive_target(timeout=0.5)