# 硬件引脚配置
FAN_PIN = None  # J17接口内置PWM控制，无需GPIO
RED_LED_PIN = 2
YELLOW_LED_PIN = 3
DIGIT_SDA_PIN = 21
DIGIT_SCL_PIN = 20
DIGIT_I2C_ADDR = 0x24  # 需通过i2cdetect确认实际地址
MIC_ADC_CHANNEL = 0
# 功能阈值配置
TEMP_THRESHOLD = 28.0    # 风扇启动温度（℃）
COOLDOWN_DELAY = 60      # 风扇延迟关闭时间（秒）
FREQ_THRESHOLD = 20000   # 频率显示上限（Hz）
AUDIO_FILE_PATH = "/home/pi/audio/"  # 音频文件路径
