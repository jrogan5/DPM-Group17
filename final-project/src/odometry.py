from utils.brick import EV3UltrasonicSensor, Motor, wait_ready_sensors, reset_brick
import time
from config import *
from helper_functions import *

class Odometry:

    def __init__(self, debug=False):
        self.US_X: EV3UltrasonicSensor = EV3UltrasonicSensor(ULTRASONIC_SIDE_PORT)
        self.US_Y: EV3UltrasonicSensor = EV3UltrasonicSensor(ULTRASONIC_REAR_PORT)
        self.debug = debug
        self.avg = True

    def sample_sensor(self,US:EV3UltrasonicSensor) -> float:
        if self.avg:
            result = 0.0
            summation = 0.0
            num_samples = 25.0
            for _ in range (0,int(num_samples)):
                reading = US.get_value()
                summation += reading
            result = summation / num_samples
        else:
            result = US.get_value()
        return result

    """
    def sample_sensor(self,US:EV3UltrasonicSensor) -> float:
        return US.get_value()
    """

    def get_xy(self, direction:str) -> tuple[int, int]:
        """
        Author: James
        Date: 2024-01-01
        Purpose: Get the x and y coordinates of the robot based on the direction it is facing.
        """
        if direction == "N":
            usx_data = self.sample_sensor(self.US_X) + CEN_X # Float value in centimeters 0, capped to 255 cm
            usy_data = self.sample_sensor(self.US_Y) + CEN_Y        
        elif direction == "E":
            usy_data = MAX_Y - (self.sample_sensor(self.US_X) + CEN_X) 
            usx_data = self.sample_sensor(self.US_Y) + CEN_Y
        elif direction == "S":
            usx_data = MAX_X - (self.sample_sensor(self.US_X) + CEN_X) 
            usy_data = MAX_Y - (self.sample_sensor(self.US_Y) + CEN_Y)
        elif direction == "W":
            usy_data = self.sample_sensor(self.US_X) + CEN_X
            usx_data = MAX_X - (self.sample_sensor(self.US_Y) + CEN_Y)
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
    time.sleep(tsleep)
    pos = odometry.get_xy("N")
    print(f"coordinates: {pos}. North.")
    time.sleep(tsleep)
    pos = odometry.get_xy("E")
    print(f"coordinates: {pos}. East.")
    time.sleep(tsleep)    
    pos = odometry.get_xy("S")
    print(f"coordinates: {pos}. South.")
    time.sleep(tsleep)
    pos = odometry.get_xy("W")
    print(f"coordinates: {pos}. West. \n Done.")

