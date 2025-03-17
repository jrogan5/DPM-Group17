''' lab3_drum
This controls the drumming function of the flute.
Allows for starting/stopping drumming thread

Controls the drumming mechanism 

Authors: David Vo, James Rogan, Lucia Cai
February 14th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import time
import threading
LEFT_WHEEL = Motor("B")
RIGHT_WHEEL = Motor("C")


wait_ready_sensors(True)
    
wheel_stop_event = threading.Event()

START_BUTTON = TouchSensor(1)        
    
def rotate_continuous(wheel, speed=0, test=False):
    "run drum cycles until stopped"
    while not wheel_stop_event.is_set():
        print("Should be running")
        wheel.set_position_relative(100)
    wheel_stop_event.clear()
    
def rotate_continuous(wheel, speed=0, test=False):
    "run drum cycles until stopped"
    while not wheel_stop_event.is_set():
        print("Should be running")
        wheel.set_position_relative(100)
    wheel_stop_event.clear()
    
def rotate_right(left_wheel, right_wheel, speed=0, test=False):
    "run drum cycles until stopped"
    left_wheel.set_position_relative(295)
    right_wheel.set_position_relative(-295)
    wheel_stop_event.clear()
    
def rotate_left(left_wheel, right_wheel, speed=0, test=False):
    "run drum cycles until stopped"
    left_wheel.set_position_relative(-295)
    right_wheel.set_position_relative(295)
    wheel_stop_event.clear()
    
def move_forward_1(left_wheel, right_wheel, speed=0, test=False):
    left_wheel.set_position_relative(-630)
    right_wheel.set_position_relative(-630)
    wheel_stop_event.clear()

def hard_code_traversal(left_wheel, right_wheel, speed=0, test=False):
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(5)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(5)
    rotate_right(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(5)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(5)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(5)
    rotate_left(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(5)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    

def start_wheels(wheel, speed=0, test=False):
    "start drum thread"
    print(f"starting wheel test")
    wheel_thread = threading.Thread(target=hard_code_traversal,args=(LEFT_WHEEL, RIGHT_WHEEL, speed, test, ))
    return wheel_thread

def stop_wheel(thread):
    "stop the wheel thread"
    wheel_stop_event.set()
    thread.join()
    LEFT_WHEEL.set_position(0)
    RIGHT_WHEEL.set_position(0)
    
def wheels_init():
    "initialize the 2 wheels"
    LEFT_WHEEL.set_limits(40,360)
    RIGHT_WHEEL.set_limits(40, 360)
    LEFT_WHEEL.reset_encoder()
    RIGHT_WHEEL.reset_encoder()


if __name__ == '__main__' :
    try:
        wheels_init()
        wait_ready_sensors(True)
        while not START_BUTTON.is_pressed():
            pass
        threadl = start_wheels(LEFT_WHEEL)
        # threadr = start_wheels(RIGHT_WHEEL)
        threadl.start()
        # threadr.start()
        while True:
            pass
    except KeyboardInterrupt:
        print("Done")

    
    
    
    
    
    
    

