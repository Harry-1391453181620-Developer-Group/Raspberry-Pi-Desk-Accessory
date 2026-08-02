#!/home/harry/ras_project_1/venv/bin/python
import numpy as np
import time
from mcp3008 import MCP3008
from digit_display import TM1650
from config import *

adc = MCP3008(SPI_BUS, SPI_DEVICE)
display = TM1650()

def collect_samples():
    samples = np.zeros(MIC_SAMPLE_COUNT)
    start = time.perf_counter()
    for i in range(MIC_SAMPLE_COUNT):
        samples[i] = adc.read(MIC_CHANNEL)
    end = time.perf_counter()
    fs = MIC_SAMPLE_COUNT / (end - start)
    return samples, fs
def calculate_frequency(samples, fs):
    samples = samples - np.mean(samples)
    fft_result = np.fft.rfft(samples)
    magnitude = np.abs(fft_result)
    freq = np.fft.rfftfreq(
        len(samples),
        d=1 / fs
    )
    peak = np.argmax(magnitude)
    return freq[peak]
def main():
    print("Frequency Detect and Display System Started")
    try:
        while True:
            samples, fs= collect_samples()
            frequency = calculate_frequency(samples, fs)
            display.display_frequency(frequency)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exit")
    finally:
        display.close()
        adc.close()

if __name__ == "__main__":
    main()