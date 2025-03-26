'''
Sweep.py
Purpose: To sweep an area 45 degrees to the left and right of the robot's centerline. 
Authors:  J. Rogan
Date: March 26th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import time
import threading
from turning import execute_turn, RW_ADJ
LEFT_WHEEL = Motor("D")
RIGHT_WHEEL = Motor("C")
START_BUTTON = TouchSensor(3)        

DELAY_TURN = 1

wait_ready_sensors(True)
    
wheel_stop_event = threading.Event()

def sweep():
    execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_45")
    time.sleep(DELAY_TURN)
    execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CCW_45")
    time.sleep(DELAY_TURN)
    execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CCW_45")
    time.sleep(DELAY_TURN)  
    execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_45")
    time.sleep(DELAY_TURN)

