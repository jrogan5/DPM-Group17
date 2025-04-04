from utils.brick import EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick
import time
from config import *
from helper_functions import *

class Odometry:

    def __init__(self, debug=False):
        self.US_X: EV3UltrasonicSensor = EV3UltrasonicSensor(ULTRASONIC_SIDE_PORT)
        self.US_Y: EV3UltrasonicSensor = EV3UltrasonicSensor(ULTRASONIC_REAR_PORT)
        self.debug = debug

    def get_xy(self, direction:str) -> tuple[int, int]:
        """
        Author: James
        Date: 2024-01-01
        Purpose: Get the x and y coordinates of the robot based on the direction it is facing.
        """
        if direction == "N":
            usx_data = self.US_X.get_value() + CEN_X # Float value in centimeters 0, capped to 255 cm
            usy_data = self.US_Y.get_value() + CEN_Y        
        elif direction == "E":
            usy_data = MAX_Y - (self.US_X.get_value() + CEN_X) 
            usx_data = self.US_Y.get_value() + CEN_Y
        elif direction == "S":
            usx_data = MAX_X - (self.US_X.get_value() + CEN_X) 
            usy_data = MAX_Y - (self.US_Y.get_value() + CEN_Y)
        elif direction == "W":
            usy_data = self.US_X.get_value() + CEN_X
            usx_data = MAX_X - (self.US_Y.get_value() + CEN_Y)
        else:
            raise ValueError(f"Invalid direction: {direction}")
        return usx_data, usy_data
    
    def at_position(self, direction:str, input:tuple[float,float]):
        equal = False
        x,y = self.get_xy(direction)
        if self.debug:
            print(f"input: {input}. current: ({x},{y}).")
        if abs(input[0] - x) < POS_THRESHOLD and abs(input[1] - y) < POS_THRESHOLD:
            equal = True
        return equal


if __name__ == '__main__' :
    print("Testing mode: odometry")
    tsleep=0.1
    odometry = Odometry(debug=True)
    wait_ready_sensors(True)
    pos = odometry.get_xy("N")
    print(f"coordinates: {pos}. Rotate CW_90 Manually.")
    time.sleep(tsleep)
    pos = odometry.get_xy("E")
    print(f"coordinates: {pos}. Rotate CW_90 Manually.")
    time.sleep(tsleep)    
    pos = odometry.get_xy("S")
    print(f"coordinates: {pos}. Rotate CW_90 Manually.")
    time.sleep(tsleep)
    pos = odometry.get_xy("W")
    print(f"coordinates: {pos}. Done")

