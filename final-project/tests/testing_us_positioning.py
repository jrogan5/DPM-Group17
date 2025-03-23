#!/usr/bin/env python3

"""
Test US Positioning
Purpose: preliminary test of the dynamic position moitoring using two petpendicular US sensors.
Hardware Version: V1.1
Date: Maarch 17, 2025
Author: J. Rogan
"""

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from time import sleep


DELAY_SEC = 1  # seconds of delay between measurements
MAX_X=120 #cm
MAX_Y=120 #cm
US_SENSOR_DATA_FILE = "/home/pi/DPM-Group17/DPM-Group17/Final_Project/Testing/test_data/us_sensor.csv"


print("Program start.\nWaiting for sensors to turn on...")

TOUCH_SENSOR = TouchSensor(3)
US_X = EV3UltrasonicSensor(1)
US_Y = EV3UltrasonicSensor(2)


wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")


def collect_continuous_us_data():
    "Collect continuous data from the ultrasonic sensor between two button presses."
    try:
        output_file = open(US_SENSOR_DATA_FILE, "w")
        while not TOUCH_SENSOR.is_pressed():
            pass  # do nothing while waiting for first button press
        print("Touch sensor pressed")
        sleep(1)
        print("Starting to collect US distance samples")
        while not TOUCH_SENSOR.is_pressed():
            num = int(input("enter turn state: "))
            data = map_us_data_to_orientation(num)
            if (data is not None): # If None is given, then data collection failed that time
                print(f"({data[0]},{data[1]})\n")
                output_file.write(f"({data[0]},{data[1]})\n")
            sleep(DELAY_SEC)
    except BaseException as e:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print(f"Error occured: {e}\n")
        pass
    finally:
        output_file.close()
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

def map_us_data_to_orientation(turnstate):
    if(turnstate==0):
            usx_data = US_X.get_value()  # Float value in centimeters 0, capped to 255 cm
            usy_data = US_Y.get_value()  # Float value in centimeters 0, capped to 255 cm
    elif(turnstate==1):
            usx_data = MAX_X-US_Y.get_value()  # Float value in centimeters 0, capped to 255 cm
            usy_data = US_X.get_value()        # Float value in centimeters 0, capped to 255 cm
    elif (turnstate==2):
            usx_data = MAX_X-US_X.get_value()  # Float value in centimeters 0, capped to 255 cm
            usy_data = MAX_Y-US_Y.get_value()  # Float value in centimeters 0, capped to 255 cm      
    elif (turnstate==3):
            usx_data = US_Y.get_value()        # Float value in centimeters 0, capped to 255 cm
            usy_data = MAX_Y-US_Y.get_value()  # Float value in centimeters 0, capped to 255 cm 
    elif (turnstate==4):
            usx_data = US_Y.get_value()        # Float value in centimeters 0, capped to 255 cm
            usy_data = MAX_Y-US_X.get_value()  # Float value in centimeters 0, capped to 255 cm
    else:
        print("here")
    return usx_data, usy_data

if __name__ == "__main__":
    collect_continuous_us_data()

