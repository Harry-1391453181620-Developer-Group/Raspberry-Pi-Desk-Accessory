#!/usr/bin/env python3

import serial
import time
import threading


ser = serial.Serial(
    port="/dev/serial0",
    baudrate=9600,
    timeout=1
)


_playing = False
_thread = None


def checksum(cmd, param, ack=0x01):

    total = 0xFFFF - (
        0xFF +
        0x06 +
        cmd +
        ack +
        ((param >> 8) & 0xFF) +
        (param & 0xFF)
    ) + 1

    return (total >> 8) & 0xFF, total & 0xFF



def send_command(cmd, param=0):

    ser.reset_input_buffer()

    high = (param >> 8) & 0xFF
    low = param & 0xFF

    chkH, chkL = checksum(cmd, param)

    packet = bytes([
        0x7E,
        0xFF,
        0x06,
        cmd,
        0x01,
        high,
        low,
        chkH,
        chkL,
        0xEF
    ])

    ser.write(packet)

    time.sleep(0.2)

def read_response():
    data = ser.read(10)
    if len(data) == 10:
        return data
    return None



def set_volume(volume=30):

    send_command(0x06, volume)



def play_track(track):

    send_command(0x12, track)



def stop_audio():

    global _playing

    _playing = False

    # DFPlayer stop命令
    send_command(0x16, 0)



def _playlist_loop():

    global _playing

    playlist = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        60,
        61,
        62,
        63,
        64,
        65,
        66,
        67,
        68,
        69,
        70,
        71,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83
    ]

    while _playing:
        for track in playlist:

            if not _playing:
                break
            ser.reset_input_buffer()
            play_track(track)
            

            while _playing:
                response = read_response()
                if response:
                    if response[3] == 0x3D and response[0] == 0x7E and response[9] == 0xEF:  # 播放完成事件
                        print("Track finished playing.")
                        break
                time.sleep(0.05)
            if _playing:
                time.sleep(1)



def play_audio():

    global _playing, _thread


    if _playing:
        return


    set_volume(30)

    _playing = True


    _thread = threading.Thread(
        target=_playlist_loop,
        daemon=True
    )

    _thread.start()



def init_audio_player():

    time.sleep(2)

    set_volume(30)

    print("DFPlayer initialized")
