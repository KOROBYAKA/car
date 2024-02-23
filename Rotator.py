import time
from threading import Thread

from gpiozero import PWMOutputDevice


class Rotator(Thread):
    dt = 0.01

    def __init__(self, frequency_Hz: int = 30):
        self._command = ''
        self.running = True
        self.Left_pin = PWMOutputDevice(18, frequency=frequency_Hz)
        self.Right_pin = PWMOutputDevice(23, frequency=frequency_Hz)
        Thread.__init__(self, daemon=True)

    def __enter__(self):
        self.start()
        print("Initialized rotator thread")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.running = False
        try:
            self.join(timeout=1.0)
            print("Terminated rotator thread")
        except TimeoutError:
            print(f"Could not join {self.__class__.__name__}, explosion imminent")

    def run(self):
        while self.running:
            if self._command == 'L':
                self.Left_pin.value = 0.4
                time.sleep(self.dt)
                self.Left_pin.value = 0.2
                time.sleep(self.dt)
            elif self._command == 'R':
                self.Left_pin.value = -0.4
                time.sleep(self.dt)
                self.Left_pin.value = -0.2
                time.sleep(self.dt)
            else:
                self.Right_pin.value = 0
                self.Left_pin.value = 0

        self.Left_pin.close()
        self.Right_pin.close()


    def set_speed(self, speed: float, time_left: float):
        assert -0.5 < speed < 0.5
        #assert speed > 0, "only forward for now!!!"
        assert time_left <= 1.0, "Do not run motor for > 1 second you silly!"
        print(f"Starting motor with speed {speed} for {time_left} s")
        self._command = (speed, time_left)
