#!/usr/bin/env python3
'''
Tetting Navigation
Purpose: integrating the movement, turning, and US positioning to navigate the robot
Author(s): J. Rogan
Date: March 26th, 2025
'''

from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep
from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import threading
from turning import RW_ADJ, execute_turn
from testing_us_positioning import get_xy

# Port mapping
LEFT_WHEEL = Motor("D")
RIGHT_WHEEL = Motor("C")
TOUCH_SENSOR = TouchSensor(3)
US_X = EV3UltrasonicSensor(1)
US_Y = EV3UltrasonicSensor(2)

