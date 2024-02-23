#!/usr/bin/python3
from time import sleep
from traceback import print_exc

from Motor import Motor
from Rotator import Rotator

def main():
    sleep(5)
    try:
        with Motor() as drive_motor:
            drive_motor.set_speed(-0.4, 1.0)
            sleep(0.4)
            #raise RuntimeError("MAMA")
            sleep(5)
            drive_motor.set_speed(0.4, 1.0)
            sleep(3)
    except Exception as e:
        print(f"Caught {e}")




if __name__ == "__main__":
    main()
