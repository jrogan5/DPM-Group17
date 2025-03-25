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
    
DEFAULT_DEG = 92
DEFAULT_DPS = 360

# STATE_INIT = 0
# STATE_FIRE1 = 1
# STATE_FIRE2 = 2
curr_state = 0 #Start at inital state


def sandbag_init():
    "initialize the sandbag with limits"
    motor.set_limits(1000,DEFAULT_DPS)
    motor.reset_encoder()
    motor.set_position(0)
    print(f'Medium motor initialized with dps {DEFAULT_DPS}\n')


def sandbag_dispenser(deg,curr_state):
    "rotates the motor to move one sandbag once"
    
    if curr_state == 2:
        print("All sandbags have been dispensed")
        output = input("Do you want to restart? (y/n)")
        if output == "y":
            curr_state = 0
        elif output == "n":
            return curr_state
        else:
            print("Invalid input, please write (y/n)")
        

    curr_state += 1
    motor.set_position_relative(deg)
    print(f'Moving 1 sandbag at {deg} deg -> now in state {curr_state}\n')
    return curr_state
    

    
def sandbag_spin(dps):
    motor.set_dps(dps)
    print("Rotating continuously at {}%\n".format(dps))

def sandbag_testing_mode(curr_state):
    "Testing Mode for the sandbag dispenser"
    deg = DEFAULT_DEG
    dps = DEFAULT_DPS
    print("Testing sandbag dispenser")
    command = input("Enter command (deg, dps, spin, test): \n")
    if command == "deg":
        try:
            deg = input("\n Enter desired deg value: ")
        except (ValueError):
            print("Invalid deg")

    elif command == "dps":
        try:
            dps = input("\n Enter desired dps value: ")
        except (ValueError):
            print("Invalid dps")

    elif command == "spin":
        try:
            sandbag_spin(dps)
        except():
            print("Invalid spin")
        
    elif command == "test":
        motor.set_limits(1000,dps)
        motor.reset_encoder()
        motor.set_position(0)
        print(f'Medium motor initialized with dps {dps} -> now in state {curr_state}\n')
        while True:
            if input("Rotate once?\n") == "y" :
                curr_state = sandbag_dispenser(deg, curr_state)
    else:
        print("Invalid command, try again")
    
    
if __name__ == '__main__' :
    try:
        sandbag_init()
        mode = input("Enter mode (normal, testing)\n")
        while True:
            if mode == "normal":
                if input("Rotate once? (y)\n") == "y" :
                    curr_state = sandbag_dispenser(DEFAULT_DEG,curr_state)
                    #sandbag_loop(360) //comment this out to perform continuous rotation
            elif mode == "testing":
                sandbag_testing_mode(curr_state)
            else:
                print("Invalid mode, try again")
                mode = input("Enter mode (normal, testing)\n")
            

    except KeyboardInterrupt:
        pass
        """TODO Reset brickpi"""
        reset_brick() # Turn off everything on the brick's hardware, and reset it
