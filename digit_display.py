import time
import smbus2
from config import DIGIT_I2C_ADDR
# TM1650驱动命令定义
CMD_BRIGHTNESS = 0x80    # 亮度设置命令（0x80+0~7）
CMD_WRITE_DATA = 0x40    # 数据写入命令
CMD_DISPLAY_ADDR = 0x68  # 显示地址命令（0x68+0~3，4位数码管）
# 共阳数码管段码表（A-G+DP段，匹配TM1650逻辑）
SEG_MAP = {
    '0': 0x3f, '1': 0x06, '2': 0x5b, '3': 0x4f,
    '4': 0x66, '5': 0x6d, '6': 0x7d, '7': 0x07,
    '8': 0x7f, '9': 0x6f,
    'A': 0x77, 'B': 0x7c, 'C': 0x39, 'D': 0x5e,
    'E': 0x79, 'F': 0x71, 'P': 0x80,  # 'P'表示小数点点亮
    ' ': 0x00, '-': 0x40  # 空格和短横线
}
bus = None  # I2C总线对象
def init_display():
    """初始化TM1650数码管，包含电源去耦配置"""
    global bus
    try:
        # 打开I2C总线（1号总线，对应GPIO21/20）
        bus = smbus2.SMBus(1)
        # 设置数码管亮度为最大（0x80+7）
        bus.write_byte(DIGIT_I2C_ADDR, CMD_BRIGHTNESS + 7)
        # 电源去耦电容需物理连接在VCC和GND之间，靠近TM1650芯片
        print("数码管初始化成功")
        return True
    except FileNotFoundError:
        print("I2C总线未找到，请检查I2C是否启用")
        return False
    except smbus2.SMBusError as e:
        print(f"I2C初始化错误: {e}，请检查硬件连接")
        return False
    except Exception as e:
        print(f"初始化未知错误: {e}")
        return False
def display_text(text):
    """在4位数码管上显示文本（自动截断/补空格）"""
    if bus is None:
        print("数码管未初始化，无法显示")
        return
    # 文本处理：截断为4位并左对齐
    display_text = text[:4].ljust(4, ' ')
    # 转换为段码数组
    seg_data = [SEG_MAP.get(char.upper(), 0x00) for char in display_text]
    try:
        # 发送I2C数据块（命令+地址+段码）
        bus.write_i2c_block_data(
            DIGIT_I2C_ADDR,
            CMD_WRITE_DATA,
            [CMD_DISPLAY_ADDR] + seg_data
        )
    except smbus2.SMBusError as e:
        print(f"I2C显示错误: {e}")
    except Exception as e:
        print(f"显示异常: {e}")
def display_frequency(freq):
    """格式化显示频率值（带小数点处理）"""
    if freq is None or freq <= 0:
        display_text("----")
        return
    # 频率值处理：大于10000Hz显示为XX.Xk，否则显示XXX.XHz
    if freq >= 10000:
        display_freq = freq / 1000  # 转换为kHz
        display_text(f"{display_freq:.1f}".replace('.', 'P'))
    else:
        display_text(f"{freq:.1f}".replace('.', 'P'))
def cleanup_display():
    """关闭数码管显示并释放资源"""
    if bus is not None:
        try:
            bus.write_byte(DIGIT_I2C_ADDR, CMD_BRIGHTNESS + 0)  # 亮度设为0
            bus.close()
            print("数码管资源已清理")
        except smbus2.SMBusError as e:
            print(f"资源清理错误: {e}")
        except Exception as e:
            print(f"清理异常: {e}")
# 模块加载时自动初始化数码管
if not init_display():
    print("数码管初始化失败，程序将继续但无法显示")
