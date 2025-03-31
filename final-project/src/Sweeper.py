from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading

from color_sensor import ColorDetector
from wheels import Wheels
from sandbag import SandbagDispenser
from config import *
from helper_functions import *

class Sweeper:

    def __init__(self, debug=False):
        self.SWEEP_MOTOR: Motor = Motor(SWEEP_MOTOR_PORT)

        self.SWEEP_MOTOR.set_limits(15, 360)
        self.SWEEP_MOTOR.reset_encoder()
        
        self.SANDBAG_DISPENSER: SandbagDispenser = SandbagDispenser()
        self.DETECTOR = ColorDetector()
        self.wheels = Wheels(debug)
        wait_ready_sensors(True)


    def wait_between_moves(self)->None: # To test in Person
        time.sleep(0.15)
        while self.SWEEP_MOTOR.is_moving():
            pass
        
    def reset_sweep_position(self)->None:
        self.SWEEP_MOTOR.set_position(0)
        self.wait_between_moves()

    def sweep_motion(self):
        try:
            self.reset_sweep_position()
            curr_pos = self.SWEEP_MOTOR.get_position() 
            if -5 < curr_pos and curr_pos < 5:
                self.SWEEP_MOTOR.set_position(SWEEP_RANGE)
            else:
                self.reset_sweep_position()
            self.wait_between_moves()

        except RuntimeError:
            print("Thread ended forcibly")
        

    def full_sweep(self):
        sweep_motor_thread = threading.Thread(target=self.sweep_motion, args=(None ,))
        sweep_motor_thread.start()
        color = None
        while sweep_motor_thread.is_alive(): # To test in person
            color = self.DETECTOR.detect_color()
            if self.debug:
                print(color)
            if color in ("red, green"):
                break
            time.sleep(REFRESH_RATE)
        if color == "red":
            pos = self.SWEEP_MOTOR.get_position()
            print(pos)
            force_kill_thread(sweep_motor_thread, RuntimeError)
            self.SWEEP_MOTOR.set_position(pos)
            self.wait_between_moves()
            self.SANDBAG_DISPENSER.deploy_sandbag()
            time.sleep(2)
            self.reset_sweep_position()
        elif color == "green":
            self.wheels.execute_turn("CW_90")
            time.sleep(2)
            self.wheels.move_forward(100)
            time.sleep(2)


if __name__ == "__main__":
    sweeper = Sweeper()
    for i in range(3):
        sweeper.full_sweep()
        sweeper.wait_between_moves()
        sweeper.wheels.move_forward(70)
    # TODO: Test number of sweep for 1 square
    # TODO: Do it for it for whole Kitchen