import RPi.GPIO as GPIO
import time
import audio_player
from config import *
def button_led_control():
    """按钮事件监听与LED状态控制"""
    BUTTON_PIN = 17
    # 初始化GPIO引脚
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 内部上拉电阻
    GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)  # 备用LED控制
    print("按钮与LED控制启动，等待按钮事件...")
    last_button_state = GPIO.HIGH  # 初始状态为未按下
    debounce_time = 0  # 去抖动时间戳
    try:
        while True:
            current_state = GPIO.input(BUTTON_PIN)
            current_time = time.time()
            # 按钮去抖动处理（200ms）
            if current_state != last_button_state and (current_time - debounce_time) > 0.2:
                debounce_time = current_time
                last_button_state = current_state
                if current_state == GPIO.LOW:
                    # 按钮按下事件
                    print("按钮按下，播放音频...")
                    audio_player.play_music(1)
                    GPIO.output(YELLOW_LED_PIN, GPIO.HIGH)
                else:
                    # 按钮松开事件
                    print("按钮松开，停止音频...")
                    audio_player.stop_music()
                    GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
            time.sleep(0.05)  # 50ms循环一次
    except KeyboardInterrupt:
        print("按钮控制程序终止，清理资源...")
        audio_player.stop_music()
        GPIO.output(YELLOW_LED_PIN, GPIO.LOW)
        GPIO.cleanup()
if __name__ == "__main__":
    button_led_control()
