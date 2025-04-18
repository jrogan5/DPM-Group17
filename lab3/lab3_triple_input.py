'''lab3_triple_input
Maps touch inputs to notes, allows for combinations of inputs.

Author: Eric Deng
February 14th, 2025
'''

from utils.brick import TouchSensor, reset_brick, wait_ready_sensors
import time

TS1 = TouchSensor(1)
TS2 = TouchSensor(2)
TS3 = TouchSensor(3)

wait_ready_sensors(True)

bti = lambda x : 1 if x else 0 # boolean to int

    
# configuration should be set for x amount of time
def collect_input_int():
    num = 4*bti(TS1.is_pressed()) + 2*(TS2.is_pressed())+TS3.is_pressed()
    time.sleep(0.2)
    new_num = 4*bti(TS1.is_pressed()) + 2*(TS2.is_pressed())+TS3.is_pressed()
    if new_num == num:
        return num
    return -1
    
    
        
        

