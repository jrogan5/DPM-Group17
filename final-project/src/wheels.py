'''
Testing Wheels
Purpose: To test the movement and turning of the robot
Authors: E. Deng, J. Rogan
Date: March 26th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick, TouchSensor
import time
import threading
import sweep

from turning import execute_turn, RW_ADJ
LEFT_WHEEL = Motor("D")
RIGHT_WHEEL = Motor("C")


wait_ready_sensors(True)

    
wheel_stop_event = threading.Event()

START_BUTTON = TouchSensor(3)        
    
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
    left_wheel.set_position_relative(240)
    right_wheel.set_position_relative(-240)
    wheel_stop_event.clear()
    
def rotate_left(left_wheel, right_wheel, speed=0, test=False):
    "run drum cycles until stopped"
    left_wheel.set_position_relative(-240)
    right_wheel.set_position_relative(240)
    wheel_stop_event.clear()
    
def move_forward_1(left_wheel, right_wheel, speed=0, test=False):
    left_wheel.set_position_relative(-660)
    right_wheel.set_position_relative(-660)
    wheel_stop_event.clear()
    print("moved forward")

def hard_code_traversal(left_wheel, right_wheel, speed=0, test=False):
    time.sleep(1)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(2)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(2)
    execute_turn(left_wheel, right_wheel, "CW_90")
    time.sleep(2)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(2)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(2)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(2)
    execute_turn(left_wheel, right_wheel, "CCW_90")
    time.sleep(2)
    move_forward_1(left_wheel, right_wheel, speed=0, test=False)
    time.sleep(2)
    sweep.full_sweep(sweep.SWEEP_MOTOR)
    

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
    LEFT_WHEEL.set_limits(30,360)
    RIGHT_WHEEL.set_limits(30, 360)


def forward_move(magnitude, left_wheel, right_wheel):
    left_wheel.set_position_relative(-magnitude)
    right_wheel.set_position_relative(-magnitude+RW_ADJ)
    wheel_stop_event.clear()
    print("moved forward")


wheels_init()
wait_ready_sensors(True)

if __name__ == '__main__' :
    try:

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

    
    
    
    
    
    
    

