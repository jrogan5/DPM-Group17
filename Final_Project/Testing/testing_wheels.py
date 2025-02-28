''' lab3_drum
This controls the drumming function of the flute.
Allows for starting/stopping drumming thread

Controls the drumming mechanism 

Authors: David Vo, James Rogan, Lucia Cai
February 14th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
LEFT_WHEEL = Motor("A")
RIGHT_WHEEL = Motor("B")


wait_ready_sensors(True)
    
wheel_stop_event = threading.Event()

    
def rotate_continuous(speed=0, test=False):
    "run drum cycles until stopped"
    while not wheel_stop_event.is_set():
        LEFT_WHEEL.set_position_relative(360)
        RIGHT_WHEEL.set_position_relative(360)
            
    wheel_stop_event.clear()

def start_wheels(half_beat, test=False):
    "start drum thread"
    print(f"starting wheel test")
    wheel_thread = threading.Thread(target=rotate_continuous,args=(half_beat, test, ))
    return wheel_thread

def stop_wheel(thread):
    "stop the wheel thread"
    wheel_stop_event.set()
    thread.join()
    LEFT_WHEEL.set_position(0)
    RIGHT_WHEEL.set_position(0)
    
def wheels_init():
    "initialize the 2 wheels"
    LEFT_WHEEL.set_limits(30,360)
    LEFT_WHEEL.reset_encoder()
    RIGHT_WHEEL.set_limits(30, 360)
    RIGHT_WHEEL.set_limits(30, 360)

if __name__ == '__main__' :
    try:
        wheels_init()
        thread = start_wheels()
    except KeyboardInterrupt:
        print("Done")
        reset_brick() # Turn off everything on the brick's hardware, and reset it

    
    
    
    
    
    
    

