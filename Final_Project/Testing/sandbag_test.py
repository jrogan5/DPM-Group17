''' 
This controls the sandbag deployment mechanism.
Activates the motor to perform a rotation, which kicks a sandbag into the funnel.

Authors: David Vo, 
March 17th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
motor = Motor("B")
wait_ready_sensors(True)
    
#sandbag_stop_event = threading.Event() //to see if needed

def sandbag_cycle(deg):
    "rotates the motor to move one sandbag once"
    motor.set_position_relative(deg)
    print("Moving sandbag")
    
def sandbag_loop(dps):
    motor.set_dps(dps)
    print("Rotating continuously")
    
def sandbag_init():
    "initialize the sandbag with limits"
    motor.set_limits(100,1000)
    motor.reset_encoder()
    motor.set_position(0)
    
if __name__ == '__main__' :
    try:
        sandbag_init()
        while True:
            if input("Rotate once?\n") == "y" :
                sandbag_cycle(90)
                #sandbag_loop(360) //comment this out to perform continuous rotation

    except KeyboardInterrupt:
        pass
        """TODO Reset brickpi"""
        reset_brick() # Turn off everything on the brick's hardware, and reset it
