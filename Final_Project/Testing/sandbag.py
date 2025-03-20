''' lab3_sandbag
This controls the sandbagming function of the flute.
Allows for starting/stopping sandbagming thread

Controls the sandbagming mechanism 

Authors: David Vo, James Rogan, Lucia Cai
February 14th, 2025
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
motor = Motor("B")
wait_ready_sensors(True)
    
#sandbag_stop_event = threading.Event()

def sandbag_cycle(deg):
    "rotates the motor to move one sandbag once"
    motor.set_position_relative(deg)
    print("Moving sandbag")
    
def sandbag_loop(dps):
    motor.set_dps(dps)
    print("Rotating continuously")
# def sandbag_loop_continuous(half_beat, test=False):
#     "run sandbag cycles until stopped"
#     if test:
#         t0 = time.time()
#         test_timing_ls = []

#     while not sandbag_stop_event.is_set():
#         sandbag_cycle(half_beat)
#         if test:
#             test_timing_ls.append(round(time.time()-t0, 1))
            
#     if test:
#         print(f"The cycles happened at these timings: {test_timing_ls}")
#         delta_ls = [test_timing_ls[i]- test_timing_ls[i-1] for i in range(1, len(test_timing_ls))]
#         mean_delta = round(sum(delta_ls)/len(delta_ls), 2)
#         print(f"the mean frequency was {mean_delta}")
#     sandbag_stop_event.clear()

# def start_sandbag(half_beat, test=False):
#     "start sandbag thread"
#     sandbag_stop_event = threading.Event()
#     print(f"starting with f {half_beat}")
#     sandbag_thread = threading.Thread(target=sandbag_loop_continuous,args=(half_beat, test, ))
#     sandbag_thread.start()
#     return sandbag_thread

# def stop_sandbag(sandbag_thread):
#     "stop the sandbag thread"
#     sandbag_stop_event.set()
#     sandbag_thread.join()
    
#     motor.set_position(0)
    
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
                #sandbag_loop(360)

    except KeyboardInterrupt:
        pass
        """TODO Reset brickpi"""
        reset_brick() # Turn off everything on the brick's hardware, and reset it
