import time
from threading import Thread

from gpiozero import PWMOutputDevice


class Motor(Thread):
    dt = 0.1

    def __init__(self, frequency_Hz: int = 30):
        self._command = (0.0, 0.0)
        self.running = True
        self.Forward_pin = PWMOutputDevice(17, frequency=frequency_Hz)
        self.Back_pin = PWMOutputDevice(4, frequency=frequency_Hz)
        Thread.__init__(self, daemon=True)

    def __enter__(self):
        self.start()
        print("Initialized drive motor thread")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.running = False
        try:
            self.join(timeout=1.0)
            print("Terminated drive motor thread")
        except TimeoutError:
            print(f"Could not join {self.__class__.__name__}, explosion imminent")

    def run(self):
        while self.running:
            speed, time_left = self._command
            if time_left > 0:
                if speed >= 0:
                    self.Forward_pin.value = speed
                    self.Back_pin.value = 0.0
                else:
                    self.Forward_pin.value = 0.0
                    self.Back_pin.value = abs(speed)
                time_left = max(time_left - self.dt, 0.0)
            elif speed != 0.0:
                self.Forward_pin.value = 0.0
                self.Back_pin.value = 0.0
                print("Stopping motor")
                speed = 0.0
            self._command = (speed, time_left)
            time.sleep(self.dt)

        self.Forward_pin.close()
        self.Back_pin.close()


    def set_speed(self, speed: float, time_left: float):
        assert -0.5 < speed < 0.5
        #assert speed > 0, "only forward for now!!!"
        assert time_left <= 1.0, "Do not run motor for > 1 second you silly!"
        print(f"Starting motor with speed {speed} for {time_left} s")
        self._command = (speed, time_left)



