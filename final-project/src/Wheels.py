'''
Testing Wheels
Purpose: To test the movement and turning of the robot
Authors: E. Deng, J. Rogan
Date: March 26th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import time
import threading
from config import *
import Odometry
from helper_functions import *

class Wheels():
    
    Directions: list[str] = ["N", "E", "S", "W"]
    
    MOVEMENT_MATRIX: dict = {
        33: {
            "CCW_90": (ANG_90+CCW_ADJ, -(ANG_90+CCW_ADJ)),
            "CW_90": (-ANG_90, ANG_90)
        },
        34: {
            "CCW_90": (ANG_90+CCW_ADJ + BAT_34_ADJ, -(ANG_90+CCW_ADJ + BAT_34_ADJ)),
            "CW_90": (-(ANG_90+BAT_34_ADJ), ANG_90+BAT_34_ADJ)
            }
        }
    
    def __init__(self, odometry:Odometry=None, debug=False):
        self.LEFT_WHEEL: Motor = Motor(LEFT_MOTOR_PORT)
        self.RIGHT_WHEEL: Motor = Motor(RIGHT_MOTOR_PORT)
        self.START_BUTTON: TouchSensor = TouchSensor(TOUCH_SENSOR_PORT)
        self.odometry = odometry if odometry else Odometry()
        self.debug = debug
        self.direction = "N"
        self._direction_index: int = 0
        self.wheels_init()
        wait_ready_sensors(True)
        print("Wheels are ready to use")

    def wheels_init(self):
        "initialize the 2 wheels"
        self.LEFT_WHEEL.set_limits(30,360)
        self.RIGHT_WHEEL.set_limits(30, 360)
    
    def _adjust_position(self, turn_to_execute)->None:
        if turn_to_execute == "CCW_90":
            self._direction_index = (self._direction_index-1)%4
        elif turn_to_execute == "CW_90":
            self._direction_index = (self._direction_index+1)%4
        else:
            raise RuntimeError(f"Turn command {turn_to_execute} is not supported")
        self.direction = Wheels.Directions[self._direction_index]

    def rotate_wheel(self, magnitude: int, wheel: Motor)->threading.Thread:
        thread = threading.Thread(target=wheel.set_position_relative, args=(magnitude,))
        thread.start()
        return thread

    def move_forward(self, magnitude:int)->tuple[threading.Thread]:
        left_thread = self.rotate_wheel(-magnitude, self.LEFT_WHEEL)
        right_thread = self.rotate_wheel(-magnitude+RW_ADJ, self.RIGHT_WHEEL)
        if self.debug:
            print("moved forward")
        return left_thread, right_thread
    
    def move_to_coord(self, end_pos:tuple[int, int])->None:
        start = self.odometry.get_xy(self.direction)
        x, y = end_pos
        cur_pos = start
        if abs(start[0] - x) < 1: # x difference is within 1 cm -> move in y
            if y - start[1] >= 0:
                self.face_direction("N")
            else:
                self.face_direction("S")
        elif abs(start[1] - y) < 1: # y difference is within 1 cm -> move in x
            if x - start[0] >= 0:
                self.face_direction("E")
            else:
                self.face_direction("W")
        else:
            if self.debug:
                print("Invalid coordinates given; cannot move in x and y at once.")
        if self.debug:
            print(f"Starting: {start} Moving to: {end_pos}")
        forward_move_threads = self.move_forward(150)
        while cur_pos[1] < y:
            cur_pos = self.odometry.get_xy(self.direction)
            if self.debug:
                print(f"Current position: {cur_pos}. Distance left: {cur_pos[1] - y}")
        force_kill_thread(forward_move_threads[0], RuntimeError)
        force_kill_thread(forward_move_threads[1], RuntimeError)


        if self.debug:
            print("moved to coordinates")

    def move_forward_1(self):
        self.LEFT_WHEEL.set_position_relative(-TILE_ANG)
        self.RIGHT_WHEEL.set_position_relative(-TILE_ANG)
        if self.debug:
            print("moved forward")
    
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
        self.move_forward(magnitude)
        self.wait_between_moves()
            
    def execute_turn(self, movement:str)->tuple[threading.Thread]:
        """Executes a predefined turn based on battery life."""
        if movement not in Wheels.MOVEMENT_MATRIX[BATTERY_NUM]:
            print("Invalid movement command.")
            return
        left_magnitude, right_magnitude = Wheels.MOVEMENT_MATRIX[BATTERY_NUM][movement]
        left_thread = self.rotate_wheel(left_magnitude, self.LEFT_WHEEL)
        right_thread = self.rotate_wheel(right_magnitude, self.RIGHT_WHEEL)
        self._adjust_position(movement)
        if self.debug:
            print(f"Executing {movement} with values {left_magnitude}, {right_magnitude}. ")
        return left_thread, right_thread

    def wait_between_moves(self)->None:
        time.sleep(0.15)
        while self.LEFT_WHEEL.is_moving() or self.RIGHT_WHEEL.is_moving():
            pass

    def hard_code_traversal(self)->None:
        self.move_forward(3*TILE_ANG)
        self.wait_between_moves()
        self.execute_turn("CW_90")
        self.wait_between_moves()
        self.move_forward(3*TILE_ANG)
        self.wait_between_moves()
        self.execute_turn("CCW_90")
        self.wait_between_moves()
        self.move_forward_1()
        self.wait_between_moves()
    

if __name__ == '__main__' :
    try:
        wheels = Wheels(debug=True)
        while not wheels.START_BUTTON.is_pressed():
            pass
        x,y = wheels.odometry.get_xy(wheels.direction)
        wheels.move_to_coord((x, y + 50))
        # wheels.move_forward_1()
        # wheels.wait_between_moves()
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

    
    
    
    
    
    
    

