import serial
import time
from config import *
# 初始化串口通信（DFPlayer连接到硬件串口ttyAMA0）
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)
def init_dfplayer():
    """DFPlayer初始化函数，包含完整的启动流程"""
    try:
        # 关闭并重新打开串口确保连接
        ser.close()
        ser.open()
        time.sleep(1)  # 等待模块上电稳定
        # 发送初始化命令序列
        ser.write(b'#000*\r\n')  # 停止播放
        time.sleep(0.3)
        ser.write(b'#001*\r\n')  # 音量设置为50%（0-100）
        time.sleep(0.3)
        ser.write(b'#029*\r\n')  # 播放模式设置为单曲循环
        time.sleep(0.3)
        # 读取初始化响应（可选）
        response = ser.read_all()
        if b'OK' in response:
            print("DFPlayer初始化成功")
        else:
            print("DFPlayer初始化响应异常")
    except serial.SerialException as e:
        print(f"串口初始化错误: {e}，请检查DFPlayer连接")
    except Exception as e:
        print(f"初始化未知错误: {e}")
def play_music(file_num):
    """播放指定编号的音频文件（1-99）"""
    if not 1 <= file_num <= 99:
        print("音频文件编号必须在1-99之间")
        return
    try:
        # 构造播放命令（格式：#00X*，X为文件编号）
        cmd = f'#00{file_num}*\r\n'.encode()
        ser.write(cmd)
        time.sleep(0.5)  # 等待播放响应
        # 读取播放状态（可选）
        response = ser.read_all()
        if b'PLAY' in response:
            print(f"开始播放文件: {file_num}.mp3")
        else:
            print(f"播放命令发送成功，但未收到播放响应")
    except serial.SerialException as e:
        print(f"串口播放错误: {e}")
    except Exception as e:
        print(f"播放异常: {e}")
def stop_music():
    """停止当前播放的音频"""
    try:
        ser.write(b'#000*\r\n')  # 停止播放命令
        time.sleep(0.3)
        response = ser.read_all()
        if b'STOP' in response or not ser.in_waiting:
            print("音频播放已停止")
        else:
            print("停止命令发送成功，但未收到停止响应")
    except serial.SerialException as e:
        print(f"串口停止错误: {e}")
    except Exception as e:
        print(f"停止异常: {e}")
# 模块加载时自动初始化DFPlayer
init_dfplayer()
