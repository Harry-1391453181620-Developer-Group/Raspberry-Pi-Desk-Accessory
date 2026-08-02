#!/home/harry/ras_project_1/venv/bin/python

import time
from w1thermsensor import W1ThermSensor, SensorNotReadyError

def read_temperature():
    """读取DS18B20温度值，含异常处理"""
    try:
        sensor = W1ThermSensor()
        return round(sensor.get_temperature(), 2)
    except SensorNotReadyError as e:
        print(f"温度读取运行时错误: {e}")
        return None
    except Exception as e:
        print(f"温度读取未知错误: {e}")
        return None

if __name__ == "__main__":
    print("DS18B20温度监测启动...")
    while True:
        temp = read_temperature()
        if temp is not None:
            print(f"当前温度: {temp}°C")
        else:
            print("温度读取失败，5秒后重试...")
        time.sleep(1)
