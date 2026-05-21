import time
import board
from adafruit_circuitpython_ds18x20 import DS18B20
def read_temperature():
    """读取DS18B20温度值，含异常处理"""
    try:
        # 初始化DS18B20传感器，连接到GPIO4（board.D4）
        sensor = DS18B20(board.D4)
        return round(sensor.temperature, 2)
    except RuntimeError as e:
        print(f"温度读取运行时错误: {e}")
        return None
    except Exception as e:
        print(f"温度读取未知错误: {e}")
        return None
if __name__ == "__main__":
    """独立运行时循环输出温度"""
    print("DS18B20温度监测启动...")
    while True:
        temp = read_temperature()
        if temp is not None:
            print(f"当前温度: {temp}°C")
        else:
            print("温度读取失败，5秒后重试...")
        time.sleep(5)
