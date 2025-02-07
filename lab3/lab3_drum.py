'''
Controls the drumming mechanism 
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
motor = Motor("B")
wait_ready_sensors(True)

def drum_reset_pos():
    time.sleep(1)
    motor.set_position(0)
    
def drum_cycle():
    
    
    motor.set_position(-60) # 100%
    time.sleep(0.5) # Wait to finish
    motor.set_position(0)
    time.sleep(0.5)
    print("done")
    
    
    # initalize for downstroke
    # motor.set_dps(90) # 90 deg/sec
    
    # initalize for upstroke
    #motor.set_power(-50) # Backwards 50%
    # motor.set_dps(-720) # Backwards 720 deg/sec
    
def drum_loop(n):
    i = 0
    while i < n:
        drum_cycle()
        i += 1
    
def drum_init():
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

    
    
    
    
    
    
    

