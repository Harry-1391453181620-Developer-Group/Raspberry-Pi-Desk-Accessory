#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

import audio_player
from config import *


BUTTON_PIN = 17



def button_led_control():

    GPIO.setmode(GPIO.BCM)


    GPIO.setup(
        BUTTON_PIN,
        GPIO.IN,
        pull_up_down=GPIO.PUD_UP
    )


    GPIO.setup(
        YELLOW_LED_PIN,
        GPIO.OUT
    )


    print("按钮与LED控制启动...")


    playing = False


    last_button_state = GPIO.HIGH
    debounce_time = 0


    audio_player.init_audio_player()


    try:

        while True:


            current_state = GPIO.input(BUTTON_PIN)

            now = time.time()


            if (
                current_state != last_button_state
                and
                now - debounce_time > 0.2
            ):

                debounce_time = now

                last_button_state = current_state


                if current_state == GPIO.LOW:


                    if not playing:

                        print("按钮按下：开始播放")

                        audio_player.play_audio()


                        GPIO.output(
                            YELLOW_LED_PIN,
                            GPIO.HIGH
                        )


                        playing = True


                    else:

                        print("按钮按下：停止播放")

                        audio_player.stop_audio()


                        GPIO.output(
                            YELLOW_LED_PIN,
                            GPIO.LOW
                        )


                        playing = False



            time.sleep(0.05)



    except KeyboardInterrupt:

        print("退出")

        audio_player.stop_audio()

        GPIO.output(
            YELLOW_LED_PIN,
            GPIO.LOW
        )

        GPIO.cleanup()



if __name__ == "__main__":

    button_led_control()