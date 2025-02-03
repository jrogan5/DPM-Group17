#!/usr/bin/env python3

"""
This test is used to collect data from the color sensor.
It must be run on the robot.
"""

# Add your imports here, if any
from utils.brick import EV3ColorSensor, wait_ready_sensors, TouchSensor, reset_brick
from time import sleep

DELAY_SEC = 0.01
COLOR_SENSOR_DATA_FILE = "../data_analysis/color_sensor.csv"

print("Program start.\nWaiting for sensors to turn on...")

# complete this based on your hardware setup
COLOR_SENSOR = EV3ColorSensor(3)
TOUCH_SENSOR = TouchSensor(1)


wait_ready_sensors(True) 


def collect_color_sensor_data():
    "Collect color sensor data."
   
    try:
        print("Hello")
        output_file = open(COLOR_SENSOR_DATA_FILE, "w")
        while True:
            
            sleep(DELAY_SEC)
    
            if TOUCH_SENSOR.is_pressed():
                print("PRESSED") 
                color_data = COLOR_SENSOR.get_rgb() 
                if color_data is not [None, None, None]: 
                    print(color_data)
                    output_file.write(f"{color_data}\n")
                    output_file.flush()
                sleep(DELAY_SEC)

                while TOUCH_SENSOR.is_pressed(): 
                    pass
               
    except BaseException:  
        print("Done collecting Color distance samples")
        output_file.close()
        reset_brick() 
        exit()
        
if __name__ == "__main__":
    collect_color_sensor_data()
    