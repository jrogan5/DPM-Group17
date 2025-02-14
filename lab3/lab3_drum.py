'''
Controls the drumming mechanism 
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
motor = Motor("B")
wait_ready_sensors(True)
    
drum_stop_event = threading.Event()

def drum_cycle():
    "hits the drum once"
    motor.set_position(-60) # 100%
    time.sleep(0.5) # wait to finish
    motor.set_position(0)
    time.sleep(0.5)
    #print("Hit Drum")
    
def drum_loop_continuous():
    "run drum cycles until stopped"
    while not drum_stop_event.is_set():
        drum_cycle()

def start_drum():
    "start drum thread"
    global drum_stop_event
    drum_stop_event.clear()
    drum_thread = threading.Thread(target=drum_loop_continuous)
    drum_thread.start()

def stop_drum():
    "stop the drum thread"
    global drum_stop_event
    drum_stop_event.set()
    
def drum_init():
    "initialize the drum with limits"
    motor.set_limits(30,360)
    motor.reset_encoder()
    
if __name__ == '__main__' :
    try:
        motor.set_limits(30,360)
        motor.reset_encoder()
        drum_loop(5)
        #drum_reset_pos()
        if input("float? y/n") == "y" :
            motor.float_motor()

    except KeyboardInterrupt:
        pass
        """TODO Reset brickpi"""
        reset_brick() # Turn off everything on the brick's hardware, and reset it

    
    
    
    
    
    
    

