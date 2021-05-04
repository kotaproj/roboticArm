import time
from machine import Pin, PWM

class Servo():
    def __init__(self, pin_no, duty=70, freq=50):
        self._servo = PWM(Pin(pin_no), freq=50, duty=duty)
        time.sleep(0.1)
        self._servo.duty(duty)
        return
    def set_duty(self, duty):
        self._servo.duty(duty)
        return
