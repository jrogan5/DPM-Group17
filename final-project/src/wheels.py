'''
Testing Wheels
Purpose: To test the movement and turning of the robot
Authors: E. Deng, J. Rogan
Date: March 26th, 2025
'''

from asyncio import FastChildWatcher
from turtle import forward
from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import time
import threading
from config import *
from helper_functions import *
from odometry import Odometry

class Wheels():
    
    Directions: list[str] = ["N", "E", "S", "W"]
    
    MOVEMENT_MATRIX: dict = {
        33: {
            "CCW_90": (ANG_90+CCW_ADJ, -(ANG_90+CCW_ADJ)),
            "CW_90": (-ANG_90, ANG_90),
            "CCW_10": (ANG_10+CCW_ADJ, -(ANG_10+CCW_ADJ)),
            "CW_10": (-ANG_10, ANG_10)
        },
        34: {
            "CCW_90": (ANG_90+CCW_ADJ + BAT_34_ADJ, -(ANG_90+CCW_ADJ + BAT_34_ADJ)),
            "CW_90": (-(ANG_90+BAT_34_ADJ), ANG_90+BAT_34_ADJ),
            "CCW_10": (ANG_10+CCW_ADJ+BAT_34_ADJ, -(ANG_10+CCW_ADJ+BAT_34_ADJ)),
            "CW_10": (-(ANG_10+BAT_34_ADJ), ANG_10+BAT_34_ADJ)
            }
        }
    
    def __init__(self, odometry:Odometry=None,debug=False):
        self.LEFT_WHEEL: Motor = Motor(LEFT_MOTOR_PORT)
        self.RIGHT_WHEEL: Motor = Motor(RIGHT_MOTOR_PORT)
        self.START_BUTTON: TouchSensor = TouchSensor(TOUCH_SENSOR_PORT)
        self.debug = debug
        if odometry is not None:
            self.odometry = odometry
        else:
            self.odometry: Odometry =Odometry(debug)
        self.direction = "N"
        self._direction_index: int = 0
        self.wheels_init()

    def dprint(self,msg:str):
        if self.debug:
            print("(Wheels) " + msg)

    def wheels_init(self):
        "initialize the 2 wheels"
        self.LEFT_WHEEL.set_limits(30,360)
        self.RIGHT_WHEEL.set_limits(30+RW_ADJ, 360)

    def wheels_sweep_init(self):
        self.LEFT_WHEEL.set_limits(30+SWEEP_POW_ADJ,360)
        self.RIGHT_WHEEL.set_limits(30+RW_ADJ+SWEEP_POW_ADJ, 360)

    def wheels_return_init(self):
        self.LEFT_WHEEL.set_limits(30,360)
        self.RIGHT_WHEEL.set_limits(30+1.5*RW_ADJ, 360)

    def _adjust_position(self, turn_to_execute)->None:
        if turn_to_execute == "CCW_90":
            self._direction_index = (self._direction_index-1)%4
        elif turn_to_execute == "CW_90":
            self._direction_index = (self._direction_index+1)%4
        else:
            raise RuntimeError(f"Turn command {turn_to_execute} is not supported")
        self.direction = Wheels.Directions[self._direction_index]


    def move_forward_1(self): # out-dated
        self.LEFT_WHEEL.set_position_relative(-TILE_ANG)
        self.RIGHT_WHEEL.set_position_relative(-TILE_ANG)
        if self.debug:
            print("moved forward")
    

    def rotate_wheel(self, magnitude: int, wheel: Motor):
        try:
            wheel.set_position_relative(magnitude)
            self.wait_between_moves()
            if self.debug:
                print(f"({wheel}) full magnitude rotation")
        except RuntimeError:
            print("Motor thread stopped forcibly")
        
    def move_forward(self, magnitude:int)->tuple[threading.Thread]:
        left_thread = threading.Thread(target=self.rotate_wheel, args=(-magnitude, self.LEFT_WHEEL))
        right_thread = threading.Thread(target=self.rotate_wheel, args=(-magnitude, self.RIGHT_WHEEL))
        left_thread.start()
        right_thread.start()
        if self.debug:
            print("Moving forward")
        return left_thread, right_thread

    def face_direction(self, direction):
        if direction == self.direction:
            if self.debug:
                print("No turn, same turning to same direction")
            return
        elif direction == Wheels.Directions[(self._direction_index+1)%4]:
            if self.debug:
                print(f"\'{direction}\' is right")
            self.execute_turn("CW_90")
        elif direction == Wheels.Directions[(self._direction_index-1)%4]:
            if self.debug:
                print(f"\'{direction}\' is left")
            self.execute_turn("CCW_90")
        elif direction == Wheels.Directions[(self._direction_index+2)%4]:
            if self.debug:
                print(f"\'{direction}\' is behind, turning twice")
            self.execute_turn("CW_90")
            self.wait_between_moves()
            self.execute_turn("CW_90")
        else:
            raise RuntimeError("Invalid direction given")
        self.wait_between_moves()
        
    def move_direction(self, direction, magnitude=TILE_ANG):
        self.face_direction(direction)
        threads = self.move_forward(magnitude)
        return threads
             
    def execute_turn(self, movement:str)->tuple[threading.Thread]:
        """Executes a predefined turn based on battery being used."""
        if movement not in Wheels.MOVEMENT_MATRIX[BATTERY_NUM]:
            print("Invalid movement command.")
            return
        left_magnitude, right_magnitude = Wheels.MOVEMENT_MATRIX[BATTERY_NUM][movement]
        left_thread = threading.Thread(target=self.rotate_wheel, args=(left_magnitude, self.LEFT_WHEEL))
        right_thread = threading.Thread(target=self.rotate_wheel, args=(right_magnitude, self.RIGHT_WHEEL))
        left_thread.start()
        right_thread.start()
        self._adjust_position(movement)
        if self.debug:
            print(f"Executing {movement} with values {left_magnitude}, {right_magnitude}. ")
        return left_thread, right_thread

    def wait_between_moves(self)->None:
        time.sleep(0.15)
        while self.LEFT_WHEEL.is_moving() or self.RIGHT_WHEEL.is_moving():
            pass

    def hard_code_traversal_there(self)->None:
        self.move_direction("N", 2*TILE_ANG-5)
        self.wait_between_moves()
        self.move_direction("E", 3*TILE_ANG-80)
        self.wait_between_moves()
        self.move_direction("N", 80)
        self.wait_between_moves()




    def hard_code_traversal_back(self)->None:
        self.move_direction("N", -80)
        self.wait_between_moves()
        self.move_direction("W", 3*TILE_ANG-80)
        self.wait_between_moves()
        self.move_direction("S", 2*TILE_ANG-30)
        self.wait_between_moves()

        
    def move_to_coord(self, axis:str, end_pos:tuple[int, int])->None:
        start = self.odometry.get_xy(direction=self.direction)
        x, y = end_pos
        cur_pos = start
        if self.debug:
            print(f"Starting: {start} Moving to: {end_pos}")
        # if abs(x-cur_pos) < POS_THRESHOLD:
        #     axis == "y"
        # elif abs(y-cur_pos) < POS_THRESHOLD:
        #     axis == "x"

        if axis == "y": # x difference is within  threshold -> move in y
            if y - start[1] >= 0:
                self.dprint("condition 1")
                forward_move_threads = self.move_direction("N", magnitude=5*TILE_ANG)
                while forward_move_threads[0].is_alive() and forward_move_threads[1].is_alive():
                    cur_pos = self.odometry.get_xy(direction=self.direction)
                    self.dprint(f"Current position: {cur_pos}. Moving North")
                    if cur_pos[1] > y: # +y
                        if self.debug:
                            self.dprint("here 1")
                        break
                    time.sleep(SENSOR_DELAY)
            else:
                self.dprint("condition 2")
                forward_move_threads = self.move_direction("S", magnitude=5*TILE_ANG)
                while forward_move_threads[0].is_alive():
                    cur_pos = self.odometry.get_xy(direction=self.direction)
                    print(f"Current position: {cur_pos}. Moving South")
                    if y > cur_pos[1]: # -y
                        if self.debug:
                            print("here 2")
                        break
                    time.sleep(SENSOR_DELAY)
        elif axis == "x": # y difference is within threshold -> move in x
            if x - start[0] >= 0: # +x
                self.dprint("condition 3")                
                forward_move_threads = self.move_direction("E", magnitude=5*TILE_ANG)
                while forward_move_threads[0].is_alive():
                    cur_pos = self.odometry.get_xy(direction=self.direction)
                    self.dprint(f"Current position: {cur_pos}. Moving East")
                    if cur_pos[0] > x:
                        if self.debug:
                            self.dprint("here 3")
                        break
                    time.sleep(SENSOR_DELAY)
            else:
                self.dprint("condition 4")
                forward_move_threads = self.move_direction("W", magnitude=5*TILE_ANG)
                while forward_move_threads[0].is_alive(): # -x
                    cur_pos = self.odometry.get_xy(direction=self.direction)
                    self.dprint(f"Current position: {cur_pos}. Moving West")
                    if x > cur_pos[0]:
                        if self.debug:
                            self.dprint("here 4")
                        break
                    time.sleep(SENSOR_DELAY)
            self.stop_wheels(forward_move_threads)
        else:
            if self.debug:
                self.dprint("Invalid axis given; cannot move in x and y at once.")
            return

        
        print(f"Input: {end_pos}. Reached position: {cur_pos}")
    
    def stop_wheels(self, forward_move_threads):
        if forward_move_threads[0].is_alive():
            left_kill_angle = self.LEFT_WHEEL.get_position()
            force_kill_thread(forward_move_threads[0], RuntimeError)
            self.LEFT_WHEEL.set_position(left_kill_angle)
            if self.debug:
                print("(Wheels) left thread killed")
        if forward_move_threads[1] and forward_move_threads[1].is_alive():
            right_kill_angle = self.RIGHT_WHEEL.get_position()
            force_kill_thread(forward_move_threads[1], RuntimeError)
            self.RIGHT_WHEEL.set_position(right_kill_angle)
            if self.debug:
                print("(Wheels) right thread killed")

if __name__ == '__main__' :
    try:
        print("Testing mode: wheels")
        wheels = Wheels(debug=True)
        wait_ready_sensors(True)
        while not wheels.START_BUTTON.is_pressed():
            pass
        # wheels.move_to_coord("y", (40, 40))
        # wheels.wait_between_moves()
        # wheels.face_direction("E")
        # wheels.wait_between_moves()
        # wheels.move_to_coord("x", (50, 50))
        #wheels.hard_code_traversal_there()
        time.sleep(1)
        wheels.face_direction("E")
        # while not wheels.START_BUTTON.is_pressed():
        #    pass
        time.sleep(1)
        wheels.face_direction("S")
        # while not wheels.START_BUTTON.is_pressed():
        #    pass
        time.sleep(1)
        wheels.face_direction("W")
        # while not wheels.START_BUTTON.is_pressed():
        #    pass
        time.sleep(1)
        wheels.face_direction("N")
        # while not wheels.START_BUTTON.is_pressed():
        #    pass
        time.sleep(1)
        wheels.face_direction("S")
        while not wheels.START_BUTTON.is_pressed():
           pass
        time.sleep(1)
        wheels.face_direction("E")
        while not wheels.START_BUTTON.is_pressed():
           pass
        time.sleep(1)
        wheels.face_direction("W")
        wheels.wait_between_moves()
        # wheels.execute_turn("CCW_90")
        # wheels.wait_between_moves()
        # wheels.execute_turn("CW_90")
        # wheels.wait_between_moves()
        # wheels.move_forward(TILE_ANG)
        # wheels.hard_code_traversal()
        
        while True:
            pass
    except KeyboardInterrupt:
        print("Done")

    
    
    
    
    
    
    

