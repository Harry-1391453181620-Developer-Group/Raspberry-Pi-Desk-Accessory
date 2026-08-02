import spidev

class MCP3008:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0
    def read(self, channel):
        if channel < 0 or channel > 7:
            raise ValueError("Channel must be an integer between 0 and 7")
        cmd = [
            1,
            (8 + channel) << 4,
            0
        ]
        adc = self.spi.xfer2(cmd)
        value = ((adc[1] & 3) << 8) | adc[2]
        return value
    def close(self):
        self.spi.close()