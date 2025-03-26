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
from testing_wheels import forward_move
from testing_us_positioning import get_xy

# Port mapping
LEFT_WHEEL = Motor("D")
RIGHT_WHEEL = Motor("C")
TOUCH_SENSOR = TouchSensor(3)
US_X = EV3UltrasonicSensor(1)
US_Y = EV3UltrasonicSensor(2)

# Path definition
PATH = [(x, 50), (70, y), (x, 70), (120, 0), (0, 0)]

def move_to_room():
    start_pos = get_xy(0)
    cur_pos = start_pos
    print("Start position: ", start_pos)
    while cur_pos[1] < PATH[0][1]:
        forward_move(50, LEFT_WHEEL, RIGHT_WHEEL)
        sleep(0.75)
        prev_pos = cur_pos
        cur_pos = get_xy(0)
        print("Current position: ", cur_pos)
        if (abs(cur_pos[1] - prev_pos[1]) > 3):
            if (cur_pos[1] > prev_pos[1]):
                execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CCW_15")
                sleep(0.75)
            if (cur_pos[1] < prev_pos[1]):
                execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_15")
                sleep(0.75)
    print("Reached 1st 90 degree turn.")

    execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_90")
    sleep(0.75)

    while cur_pos[1] < PATH[1][1]:
        forward_move(50, LEFT_WHEEL, RIGHT_WHEEL)
        sleep(0.75)
        prev_pos = cur_pos
        cur_pos = get_xy(0)
        print("Current position: ", cur_pos)
        if (cur_pos[0] > prev_pos[0]):
            execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CCW_15")
            sleep(0.75)
        if (cur_pos[0] < prev_pos[0]):
            execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_15")
            sleep(0.75)