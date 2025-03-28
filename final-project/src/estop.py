#!/usr/bin/env python3

"""
EStop module for the Firefighter Rescue Robot.
Immediately stops all robot threads/operations when triggered.

Author: Lucia Cai
Date: March 27, 2025
"""

from utils.brick import TouchSensor, reset_brick, wait_ready_sensors
import time
import os
from config import TOUCH_SENSOR_PORT;


class Estop:

    def __init__(self):

        try: 
            self.sensor = TouchSensor(TOUCH_SENSOR_PORT)
            self.running = False
        except Exception as e:
            print(f"Error initializing estop: {e}")

        else:
            print(f"Initializing 'ESTOP' [{os.path.basename(__file__)}] | Port: [{TOUCH_SENSOR_PORT}]")
        
    
    def start(self):
        self.running = True
        print("Monitoring for EStop...\n")
        while self.running:
            if self.sensor.is_pressed():
                print("EStop Activated!\n")
                self.running = False
                raise KeyboardInterrupt 

            time.sleep(1)

    def stop(self):
        self.running = False
        print("EStop deactivated.")
             

if __name__ == "__main__":

    print("TESTING MODE: EStop")

    try:
        estop = Estop()
        wait_ready_sensors(True)
        estop.start()

    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nTesting mode interrupted.")
    finally:
        estop.stop()
        reset_brick()
        print("EStop test completed.")