from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading

from color_sensor import ColorDetector
from wheels import Wheels
from sandbag import SandbagDispenser
from config import *
from helper_functions import *


class Sweeper:

    def __init__(self, debug=False, wheels=None):
        self.SWEEP_MOTOR: Motor = Motor(SWEEP_MOTOR_PORT)

        self.SWEEP_MOTOR.set_limits(SWEEP_MOTOR_LIMIT, 360)
        self.SWEEP_MOTOR.reset_encoder()
        
        self.SANDBAG_DISPENSER: SandbagDispenser = SandbagDispenser()
        self.DETECTOR = ColorDetector()
        if wheels == None:
            self.wheels = Wheels(debug)
        else:
            self.wheels = wheels
        self.debug = debug
        wait_ready_sensors(True)


    def wait_between_moves(self)->None: # To test in Person
        time.sleep(0.15)
        while self.SWEEP_MOTOR.is_moving():
            pass
        self.wheels.wait_between_moves()
        
    def reset_sweep_position(self)->None:
        self.SWEEP_MOTOR.set_position(0)
        self.wait_between_moves()

    def sweep_motion(self):
        try:
            curr_pos = self.SWEEP_MOTOR.get_position() 
            if -5 < curr_pos and curr_pos < 5:
                self.SWEEP_MOTOR.set_position(SWEEP_RANGE)
            else:
                self.reset_sweep_position()
            self.wait_between_moves()

        except RuntimeError:
            print("Thread ended forcibly")
        

    def full_sweep(self):
        sweep_motor_thread = threading.Thread(target=self.sweep_motion)
        sweep_motor_thread.start()
        color = None
        if self.debug:
            print("full sweep started")
        while sweep_motor_thread.is_alive(): # To test in person
            color = self.DETECTOR.print_color()
            #if self.debug:
                #print(color)
            if color in ("red, green"):
                break
            if type(REFRESH_RATE) == str and REFRESH_RATE.lower() != "unlimited":
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
        elif color == "unused":
            self.wheels.execute_turn("CW_90")
            self.wait_between_moves()
            self.wheels.move_forward(100)
            self.wait_between_moves()
            
    def move_and_sweep(self, num_cycles=1, magnitude=40)->None:
        for _ in range(num_cycles):
            self.full_sweep()
            self.wait_between_moves()
            self.wheels.move_forward(magnitude)
            time.sleep(0.1)
        sweeper.reset_sweep_position()
        


if __name__ == "__main__":
    sweeper = Sweeper(debug=True)
    #sweeper.sweep_motion()
    #sweeper.wait_between_moves()
    #sweeper.sweep_motion()
    sweeper.move_and_sweep(3)


    # TODO: Test number of sweep for 1 square
    # TODO: Do it for it for whole Kitchen

