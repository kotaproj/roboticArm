import time
from machine import Pin


class Stepper():
    def __init__(self,  number_of_steps,
                 motor_pin_1, motor_pin_2, motor_pin_3, motor_pin_4):
        self.step_number = 0                   # which step the motor is on
        self.direction = 0                     # motor direction
        self.last_step_time = 0                # time stamp in us of the last step taken
        self.number_of_steps = number_of_steps  # total number of steps for this motor

        # setup the pins on the microcontroller:
        self.motor_pin_1 = Pin(motor_pin_1, Pin.OUT)
        self.motor_pin_2 = Pin(motor_pin_3, Pin.OUT)
        self.motor_pin_3 = Pin(motor_pin_2, Pin.OUT)
        self.motor_pin_4 = Pin(motor_pin_4, Pin.OUT)

        # pin_count is used by the stepMotor() method:
        self.pin_count = 4

        self.set_speed()
        return

    def set_speed(self, what_speed=10):
        ''' Sets the speed in revs per minute
        '''
        self.step_delay = 60 * 1000 * 1000 // self.number_of_steps // what_speed
        return

    def step(self, steps_to_move, auto_stop=True):
        ''' Moves the motor steps_to_move steps.  If the number is negative,
            the motor moves in the reverse direction.
        '''
        steps_left = abs(steps_to_move)  # how many steps to take

        # determine direction based on whether steps_to_mode is + or -:
        self.direction = 1 if steps_to_move > 0 else 0

        # decrement the number of steps, moving one step each time:
        while steps_left > 0:
            now = time.ticks_us()
            # move only if the appropriate delay has passed:
            if time.ticks_diff(now, self.last_step_time) >= self.step_delay:
                # get the timeStamp of when you stepped:
                self.last_step_time = now
                # increment or decrement the step number,
                # depending on direction:
                if self.direction == 1:
                    self.step_number += 1
                    if self.step_number == self.number_of_steps:
                        self.step_number = 0
                else:
                    if self.step_number == 0:
                        self.step_number = self.number_of_steps
                    self.step_number -= 1

                # decrement the steps left:
                steps_left -= 1
                # step the motor to step number 0, 1, 2, 3
                self._step_motor(self.step_number % 4)

        if auto_stop:
            self.stop()
        return

    def _step_motor(self, this_step):
        ''' Moves the motor forward or backwards.
              if (this->pin_count == 4) {
        '''
        # 1010
        if this_step == 0:
            self.motor_pin_1.value(True)
            self.motor_pin_2.value(False)
            self.motor_pin_3.value(True)
            self.motor_pin_4.value(False)
        # 0110
        elif this_step == 1:
            self.motor_pin_1.value(False)
            self.motor_pin_2.value(True)
            self.motor_pin_3.value(True)
            self.motor_pin_4.value(False)
        # 0101
        elif this_step == 2:
            self.motor_pin_1.value(False)
            self.motor_pin_2.value(True)
            self.motor_pin_3.value(False)
            self.motor_pin_4.value(True)
        # 1001
        elif this_step == 3:
            self.motor_pin_1.value(True)
            self.motor_pin_2.value(False)
            self.motor_pin_3.value(False)
            self.motor_pin_4.value(True)
        return

    def stop(self):
        self.motor_pin_1.value(False)
        self.motor_pin_2.value(False)
        self.motor_pin_3.value(False)
        self.motor_pin_4.value(False)
        return
