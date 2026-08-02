#!/home/harry/ras_project_1/venv/bin/python
import time
import smbus2
from config import *

SEG_MAP = {
    '0': 0x3f, '1': 0x06, '2': 0x5b, '3': 0x4f,
    '4': 0x66, '5': 0x6d, '6': 0x7d, '7': 0x07,
    '8': 0x7f, '9': 0x6f,
    'A': 0x77, 'B': 0x7c, 'C': 0x39, 'D': 0x5e,
    'E': 0x79, 'F': 0x71,
    ' ': 0x00, '-': 0x40
}

class TM1650:
    def __init__(self):
        self.bus = smbus2.SMBus(I2C_BUS)
        self.control_addr = TM1650_CTRL
        self.digits = TM1650_DIGITS
        self.turn_on()
        self.clear()
    def turn_on(self):
        self.bus.write_byte(self.control_addr, 0x01)
    def turn_off(self):
        self.bus.write_byte(self.control_addr, 0x00)
    def clear(self):
        for addr in self.digits:
            self.bus.write_byte(addr, 0x00)
    def set_brightness(self, level):
        if level < 0:
            level = 0
        if level > 7:
            level = 7
        value = 0x01 | (level << 4)
        self.bus.write_byte(self.control_addr, value)
    def display_raw(self, seg_list):
        for addr, seg in zip(self.digits, seg_list):
            self.bus.write_byte(addr, seg)
    def display_text(self, text):
        text = str(text)
        text = text[:4].ljust(4)
        segs = []
        for c in text.upper():
            segs.append(SEG_MAP.get(c, 0x00))
        self.display_raw(segs)
    def display_number(self, number):
        number = int(number)
        if number > 9999:
            number = 9999
        if number < 0:
            number = 0
        self.display_text(f"{number:4d}")
    def display_frequency(self, freq):
        if freq <= 0:
            self.display_text("----")
            return
        if freq < 10000:
            self.display_number(round(freq))
        else:
            self.display_text("AAAA")
    def close(self):
        self.clear()
        self.turn_off()
        self.bus.close()