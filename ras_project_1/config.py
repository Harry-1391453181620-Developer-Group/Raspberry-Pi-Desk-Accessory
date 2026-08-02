#!/home/harry/ras_project_1/venv/bin/python
#led
RED_LED_PIN = 20
YELLOW_LED_PIN = 21

#TM1650
#I2C
I2C_BUS = 1
#TM1650 control address
TM1650_CTRL = 0x24
#TM1650 digit addresses
TM1650_DIGITS = [
    0x34,
    0x35,
    0x36,
    0x37
]

#MCP3008 SPI
SPI_BUS = 0
SPI_DEVICE = 0
MIC_CHANNEL = 0

#Audio Sampling
MIC_SAMPLE_RATE = 8000
MIC_SAMPLE_COUNT = 1024
MAX_DISPLAY_FREQ = 9999

# Tempreature control (DS18B20)
TEMP_THRESHOLD = 28.0
COOLDOWN_DELAY = 60

#Audio player
AUDIO_FILE_PATH = "/home/harry/audio/"  # 音频文件路径