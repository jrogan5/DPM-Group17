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
motor = Motor("B")
wait_ready_sensors(True)
    
drum_stop_event = threading.Event()

def drum_cycle(half_beat):
    "hits the drum once"
    motor.set_position(-60) # 100%
    time.sleep(half_beat) # wait to finish
    motor.set_position(0)
    time.sleep(half_beat)
    #print("Hit Drum")
    
def drum_loop_continuous(half_beat):
    "run drum cycles until stopped"
    while not drum_stop_event.is_set():
        drum_cycle(half_beat)
    drum_stop_event.clear()

def start_drum(half_beat):
    "start drum thread"
    drum_stop_event = threading.Event()
    print(f"starting with f {half_beat}")
    drum_thread = threading.Thread(target=drum_loop_continuous,args=(half_beat,))
    drum_thread.start()
    return drum_thread

def stop_drum(drum_thread):
    "stop the drum thread"
    drum_stop_event.set()
    drum_thread.join()
    
    motor.set_position(0)
    
def drum_init():
    "initialize the drum with limits"
    motor.set_limits(30,360)
    motor.reset_encoder()
    
if __name__ == '__main__' :
    try:
        motor.set_limits(30,360)
        motor.reset_encoder()
        # drum_loop(5)
        #drum_reset_pos()
        if input("float? y/n") == "y" :
            motor.float_motor()

    except KeyboardInterrupt:
        pass
        """TODO Reset brickpi"""
        reset_brick() # Turn off everything on the brick's hardware, and reset it

    
    
    
    
    
    
    

