'''
This file contains the code for user to our music device
using input from 3 tactile switches.
'''

from utils.brick import TouchSensor, reset_brick, wait_ready_sensors
import time

TS1 = TouchSensor(1)
TS2 = TouchSensor(2)
TS3 = TouchSensor(3)

wait_ready_sensors(True)

bti = lambda x : 1 if x else 0

    
# configuration should be set for x amount of time
def collect_input_data():

    num = 4*bti(TS1.is_pressed()) + 2*(TS2.is_pressed())+TS3.is_pressed()
    time.wait(0.2)
    new_num = 4*bti(TS1.is_pressed()) + 2*(TS2.is_pressed())+TS3.is_pressed()
    if new_num == num:
        return num
    return -1
    
    
        
        

