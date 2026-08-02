from multiprocessing import Process
import runpy
import time


def run_file(filename):
    runpy.run_path(filename, run_name="__main__")


if __name__ == "__main__":


    files = [
        "button_led.py",
        "fan_relay.py",
        "sound_freq.py"
    ]


    processes = []


    for f in files:

        p = Process(
            target=run_file,
            args=(f,)
        )

        p.start()

        processes.append(p)

        time.sleep(2)   # 关键


    for p in processes:
        p.join()