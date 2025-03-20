#!/usr/bin/env python3

"""
Detect colors from the color sensor. Detect fires (RED) and print out when detected.
It must be ran on the robot.
Authors: David Vo, 
March 17th, 2025
"""

from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY_SEC = 0.05

print("Program start.\nWaiting for sensors to turn on...")

COLOR_SENSOR = EV3ColorSensor(2)

wait_ready_sensors(True) 

def loop_red():
    """Continuously checks for red color and prints when detected"""
    try:
        # Set sensor to RGB mode for more accurate red detection
        COLOR_SENSOR.set_mode(COLOR_SENSOR.Mode.ID)
        
        while True:
            color_data = COLOR_SENSOR.get_rgb()
            r, g, b = color_data
            #print(color_data)
            if r > 1.5 * g and r > 1.5 * b and r > 100:
               print(f"Red detected with {color_data}")
            #print(color_data)
        
        
    except Exception as e:
        print(f"Error in red detection: {e}")
    finally:
        reset_brick()
        print("Program terminated")

if __name__ == "__main__":
    while True:
        user_input = input("Would you like to start red color detection? (y/n): ").lower()
        if user_input == 'y':
            loop_red()
            break
        elif user_input == 'n':
            print("Program cancelled by user")
            reset_brick()
            break
        else:
            print("Please enter 'y' or 'n'")
