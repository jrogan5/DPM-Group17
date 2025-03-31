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

class Wheels():
    
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
    
    def __init__(self, debug=False):
        self.LEFT_WHEEL: Motor = Motor(LEFT_MOTOR_PORT)
        self.RIGHT_WHEEL: Motor = Motor(RIGHT_MOTOR_PORT)
        self.START_BUTTON: TouchSensor = TouchSensor(TOUCH_SENSOR_PORT)
        self.debug = debug
        self.wheels_init()
        wait_ready_sensors(True)
        print("Wheels are ready to use")

    def wheels_init(self):
        "initialize the 2 wheels"
        self.LEFT_WHEEL.set_limits(30,360)
        self.RIGHT_WHEEL.set_limits(30, 360)

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

    def move_forward_1(self):
        self.LEFT_WHEEL.set_position_relative(-TILE_ANG)
        self.RIGHT_WHEEL.set_position_relative(-TILE_ANG)
        if self.debug:
            print("moved forward")
            
    def execute_turn(self, movement:str)->tuple[threading.Thread]:
        """Executes a predefined turn based on battery life."""
        if movement not in Wheels.MOVEMENT_MATRIX[BATTERY_NUM]:
            print("Invalid movement command.")
            return
        left_magnitude, right_magnitude = Wheels.MOVEMENT_MATRIX[BATTERY_NUM][movement]
        left_thread = self.rotate_wheel(left_magnitude, self.LEFT_WHEEL)
        right_thread = self.rotate_wheel(right_magnitude, self.RIGHT_WHEEL)
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
        wheels.move_forward_1()
        wheels.wait_between_moves()
        wheels.execute_turn("CCW_90")
        wheels.wait_between_moves()
        wheels.execute_turn("CW_90")
        wheels.wait_between_moves()
        wheels.move_forward(TILE_ANG)
        # wheels.hard_code_traversal()
        
        while True:
            pass
    except KeyboardInterrupt:
        print("Done")

    
    
    
    
    
    
    

