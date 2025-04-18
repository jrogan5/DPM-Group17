from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
from config import *
from helper_functions import *


class Sweeper:

    def __init__(self, debug=False):
        self.SWEEP_MOTOR: Motor = Motor(SWEEP_MOTOR_PORT)

        self.SWEEP_MOTOR.set_limits(SWEEP_MOTOR_LIMIT, 360)
        self.SWEEP_MOTOR.reset_encoder()
        self.sweeping_on=False
        self.hard_sweep=True
        self.debug = debug
        wait_ready_sensors(True)

    def dprint(self,msg:str):
        if self.debug:
            print("(Sweeper) " + msg)

    def wait_between_moves(self)->None: # To test in Person
        time.sleep(0.15)
        while self.SWEEP_MOTOR.is_moving():
            pass
                    
    def reset_sweep_position(self)->None:
        self.SWEEP_MOTOR.set_position(0)
        self.wait_between_moves()

    def sweep_motion(self):
        try:
            while self.sweeping_on:
                if abs(self.SWEEP_MOTOR.get_position()) < 10: # If the sweeper is starting in the correct position
                    self.dprint("sweep range set")
                    self.SWEEP_MOTOR.set_position(SWEEP_RANGE)
                else:
                    self.dprint("sweep range reset")
                    self.reset_sweep_position()
                    self.sweeping_on = False # One iteration
                    if abs(self.SWEEP_MOTOR.get_position()) >= 10:
                        self.SWEEP_MOTOR.set_position(-2)
                        self.wait_between_moves()
                        self.SWEEP_MOTOR.reset_encoder()
                time.sleep(REFRESH_RATE)
                self.wait_between_moves()
            print("(Sweeper) Sweeping is turned off")
        except RuntimeError:
            print("(Sweeper) Thread ended forcibly")
        
    def sweep(self)->threading.Thread:
        self.sweep_motion_thread = threading.Thread(target=self.sweep_motion)
        self.sweep_motion_thread.start()
        return self.sweep_motion_thread

    def kill_sweep(self, sweep_thread):
        if sweep_thread.is_alive():    
            pos = self.SWEEP_MOTOR.get_position()
            print(pos)
            force_kill_thread(sweep_thread, RuntimeError)
            self.SWEEP_MOTOR.set_position(pos)
            self.sweeping_on = False
            self.wait_between_moves()
            self.dprint("sweep motion killed")
        else:
            self.dprint("WARNING: Called kill_sweep without an active thread")

    def full_sweep(self):
        time.sleep(0.1)
        sweep_motor_thread = threading.Thread(target=self.sweep_motion)
        sweep_motor_thread.start()
        color = None
        if self.debug:
            print("full sweep started")
        while sweep_motor_thread.is_alive(): # To test in person
            color = self.DETECTOR.print_color()
            #if self.debug:
                #print(color)
            if color == "red":
                break
            if type(REFRESH_RATE) == str and REFRESH_RATE.lower() == "unlimited":
                continue    
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
        while sweep_motor_thread.is_alive():
            pass
            
    # def move_and_sweep(self, num_cycles=1, magnitude=40)->None:
    #     for _ in range(num_cycles):
    #         self.full_sweep()
    #         self.wait_between_moves()
    #         self.wheels.move_forward(magnitude)
    #         time.sleep(0.1)
    #     sweeper.reset_sweep_position()
        


if __name__ == "__main__":
    try:
        sweeper = Sweeper(debug=True)
        for i in range (0,10):
            print("restarting")
            sweeper.sweeping_on = True
            thread = sweeper.sweep()
            if not thread.is_alive():
                sweeper.dprint("Failed to create a thread. Exiting.")
                raise RuntimeException
            wait(1)
            if i == 5:
                sweeper.kill_sweep(thread)
                break
            while thread.is_alive():
                pass
            wait(0.5)
            print("Thread ended")
            print(i)
    except Exception as e:
        print(f"Raised: {e}")
    finally:
        print("exiting")
    #sweeper.sweep_motion()
    #sweeper.wait_between_moves()
    #sweeper.sweep_motion()
    # sweeper.move_and_sweep(7)


    # TODO: Test number of sweep for 1 square
    # TODO: Do it for it for whole Kitchen

