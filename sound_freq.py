import RPi.GPIO as GPIO
import numpy as np
from scipy.fftpack import fft
import time
import spidev
from config import MIC_ADC_CHANNEL, FREQ_THRESHOLD
from digit_display import display_frequency
# 初始化SPI总线（用于MCP3008通信）
spi = spidev.SpiDev()
spi.open(0, 0)  # 打开SPI0通道0
spi.max_speed_hz = 1000000  # 1MHz时钟频率
# 音频采样参数
SAMPLE_RATE = 44100  # 采样率（Hz）
SAMPLE_SIZE = 2048   # 采样点数
SAMPLING_INTERVAL = 1 / SAMPLE_RATE  # 采样间隔（秒）
def read_adc(channel):
    """读取MCP3008指定通道的ADC值（0-1023）"""
    if not 0 <= channel <= 7:
        print("ADC通道必须在0-7之间")
        return 0
    # 构造SPI命令字节（单端模式）
    cmd = 0x01 << 7 | (channel << 4)
    resp = spi.xfer2([1, cmd, 0])
    # 解析返回值（10位ADC）
    return ((resp[1] & 0x03) << 8) | resp[2]
def collect_sound_data():
    """采集麦克风信号并转换为数字信号"""
    data = []
    for _ in range(SAMPLE_SIZE):
        # 读取ADC值并转换为±512范围内的信号
        adc_value = read_adc(MIC_ADC_CHANNEL)
        data.append(adc_value - 512)
    return np.array(data)
def calculate_frequency(data):
    """通过FFT计算声波频率"""
    try:
        # 执行快速傅里叶变换
        yf = fft(data)
        # 计算频率轴（只取正半轴）
        xf = np.linspace(0.0, SAMPLE_RATE/2, SAMPLE_SIZE//2)
        # 找到幅度最大的频率分量
        yf_abs = np.abs(yf[0:SAMPLE_SIZE//2])
        max_idx = np.argmax(yf_abs)
        freq = xf[max_idx]
        # 过滤无效频率（20Hz-20kHz范围内）
        return freq if 20 <= freq <= FREQ_THRESHOLD else 0
    except ValueError as e:
        print(f"FFT计算值错误: {e}")
        return 0
    except Exception as e:
        print(f"频率计算异常: {e}")
        return 0
def main():
    """频率检测主函数，循环采集并显示频率"""
    print("声波频率检测系统启动...")
    print("正在初始化麦克风和FFT计算...")
    try:
        while True:
            # 采集声音数据
            sound_data = collect_sound_data()
            # 计算频率
            frequency = calculate_frequency(sound_data)
            # 显示频率
            if frequency > 0:
                print(f"检测到频率: {frequency:.1f} Hz")
                display_frequency(frequency)
            else:
                print("未检测到有效频率")
                display_frequency(0)
            time.sleep(0.5)  # 每0.5秒更新一次
    except KeyboardInterrupt:
        print("频率检测程序终止，清理资源...")
    finally:
        # 清理资源
        spi.close()
        GPIO.cleanup()
if __name__ == "__main__":
    main()
