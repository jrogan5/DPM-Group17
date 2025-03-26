#!/usr/bin/env python3

"""
Test Navigation and Path Correction
Purpose: preliminary test of using position data to conform to a pre-set path
Hardware Version: V1.1
Date: Maarch 26, 2025
Author: J. Rogan
"""

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep
from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import threading
import test_us_positioning as us_pos
import testing_wheels as wheels

START_BUTTON = TouchSensor(3)   
LEFT_WHEEL = Motor("B")
RIGHT_WHEEL = Motor("C")
BATTERY_LIFE = 100 # percent

WHEEL_RADUIS = 2 #cm

wait_ready_sensors(True)
    
wheel_stop_event = threading.Event()

def x_move_to_position(end_x, turnstate):
    """
    Move the robot from a starting x to a finishing x based on ultrasonic sensor data
    """
    # get the starting position
    start_pos = us_pos.orient(turnstate)
    start_x = start_pos[0]
    start_y = start_pos[1]
    end_x - start_x = x_diff

    if x_diff == 0:
        print("Already at position")
        return
    else: 
        # move to the desired position
        wheels.move_straight(x_diff + 3, LEFT_WHEEL, RIGHT_WHEEL) # overshoot by 3cm for safety
        while x_diff > 0:
            cur_pos = us_pos.orient(turnstate)
            x_diff = end_x - cur_x
            
            sleep(0.1)




    def move_straight(dist_cm, left_wheel, right_wheel, speed=0, test=False):
        """
        Move the robot forward a specified distance, in cm
        Date: 2025-03-26
        Author: J. Rogan
        """
        angle_disp = dist_cm * 360 / (2 * 3.14159 * WHEEL_RADUIS)
        left_wheel.set_position_relative(angle_disp)
        right_wheel.set_position_relative(angle_disp)


    def correct_path(start_pos, cur_pos, move_dir):
        """
        Correct the path of the robot, travelling straight,
        based on measurement of the other axis. 
        Date: 2025-03-26
        Author: J. Rogan
        """

        x_dev = cur_pos[0] - start_pos[0]
        y_dev = cur_pos[1] - start_pos[1]

        if move_dir == 0: # wanting to move in x
            if y_dev 


