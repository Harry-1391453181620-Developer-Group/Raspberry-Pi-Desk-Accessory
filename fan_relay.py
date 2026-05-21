import time
import ds18b20
import RPi.GPIO as GPIO
import subprocess
from config import *
def fan_control():
    """风扇控制主逻辑，基于温度阈值调节转速"""
    # 初始化GPIO和状态变量
    red_led = RED_LED_PIN
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(red_led, GPIO.OUT)
    last_active = time.time()  # 记录最后一次高温触发时间
    fan_speed = 0  # 0-100%转速
    try:
        print("风扇控制系统启动...")
        while True:
            # 读取温度并显示
            temp = ds18b20.read_temperature()
            if temp is not None:
                print(f"当前温度: {temp}°C | 风扇转速: {fan_speed}%")
            else:
                print("温度读取失败，使用默认阈值控制风扇")
            # 温度-转速逻辑控制
            if temp is not None and temp >= TEMP_THRESHOLD:
                # 温度超过阈值，全速运转并点亮红灯
                fan_speed = 100
                GPIO.output(red_led, GPIO.HIGH)
                last_active = time.time()
            else:
                if (time.time() - last_active) < COOLDOWN_DELAY:
                    # 温度下降但仍在冷却延迟内，半速运转
                    fan_speed = 50
                    GPIO.output(red_led, GPIO.HIGH)
                else:
                    # 冷却延迟结束，风扇停止并熄灭红灯
                    fan_speed = 0
                    GPIO.output(red_led, GPIO.LOW)
            # 通过系统接口设置风扇转速
            set_fan_speed(fan_speed)
            time.sleep(5)  # 每5秒检测一次
    except KeyboardInterrupt:
        print("风扇控制程序终止，清理资源...")
        set_fan_speed(0)
        GPIO.output(red_led, GPIO.LOW)
        GPIO.cleanup()
def set_fan_speed(speed_percent):
    """通过fancontrol工具设置风扇PWM转速（0-100%）"""
    try:
        # 确保fancontrol服务运行
        subprocess.run(["systemctl", "start", "rpi-fan-control"], check=True)
        # 将百分比转换为0-255的PWM值（J17接口支持）
        pwm_value = int(speed_percent * 255 / 100)
        with open("/sys/devices/pwm-fan/target_pwm", "w") as f:
            f.write(str(pwm_value))
    except subprocess.CalledProcessError as e:
        print(f"风扇服务启动失败: {e}")
    except Exception as e:
        print(f"风扇转速设置错误: {e}")
if __name__ == "__main__":
    fan_control()
