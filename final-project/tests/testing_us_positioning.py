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
TUNING_X= 3.4 # ((12.8-9.4)+(15.7-12.3))/2
TUNING_Y= 3.3 # ((14.8-11.6)+(16.5-13.2))/2
MAX_X=120 + TUNING_X #cm (see test report for derivation of tuning parameters)
MAX_Y=120 + TUNING_Y #cm
CEN_X=4.8  #cm from face of US_X, plus an additional tuning offset
CEN_Y=8.4  #cm from face of US_Y, plus an additional tuning offset

US_SENSOR_DATA_FILE = "/home/pi/DPM-Group17/DPM-Group17/final-project/tests/test_data/us_sensor.csv"


print("Program start.\nWaiting for sensors to turn on...")

TOUCH_SENSOR = TouchSensor(3)
US_X = EV3UltrasonicSensor(2)
US_Y = EV3UltrasonicSensor(1)


wait_ready_sensors(True) # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")


def collect_continuous_us_data():
    "Collect continuous data from the ultrasonic sensor between two button presses."
    try:
        # output_file = open(US_SENSOR_DATA_FILE, "w")
        while not TOUCH_SENSOR.is_pressed():
            pass  # do nothing while waiting for first button press
        print("Touch sensor pressed")
        sleep(1)
        print("Starting to collect US distance samples")
        while not TOUCH_SENSOR.is_pressed():
            num = int(input("enter turn state: "))
            data = map_us_data_to_orientation(num)
            if (data is not None): # If None is given, then data collection failed that time
                print("\n({}, {})".format(*data))
                # output_file.write(f"({data[0]},{data[1]})\n")
            sleep(DELAY_SEC)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    except Exception as e:
        print("An error occurred: {}".format(e))
    finally:
        # output_file.close()
        reset_brick() # Turn off everything on the brick's hardware, and reset it
        exit()

def map_us_data_to_orientation(turnstate):
    if(turnstate==0): # Rotation defined as 0 degrees
            usx_data = US_X.get_value() + CEN_X # Float value in centimeters 0, capped to 255 cm
            usy_data = US_Y.get_value() + CEN_Y
    elif(turnstate==1): # +90 degree rotation
            usy_data = MAX_Y - (US_X.get_value() + CEN_X) 
            usx_data = US_Y.get_value() + CEN_Y
    elif (turnstate==2): # 180 degree rotation
            usx_data = MAX_X - (US_X.get_value() + CEN_X) 
            usy_data = MAX_Y - (US_Y.get_value() + CEN_Y)
    elif (turnstate==3): # +270 degree rotation
            usy_data = US_X.get_value() + CEN_X
            usx_data = MAX_X - (US_Y.get_value() + CEN_Y)

    else:
        print("here")
    return usx_data, usy_data

if __name__ == "__main__":
    collect_continuous_us_data()

