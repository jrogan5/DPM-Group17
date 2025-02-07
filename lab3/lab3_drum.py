'''
Controls the drumming mechanism 
'''

from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
motor = Motor("C")
wait_ready_sensors(True)

def drum_reset_pos():
    time.sleep(1)
    motor.set_position(0)
    
def drum_cycle():
    motor.set_position(30) # 100%
    time.sleep(1) # Wait to finish
    motor.set_position(0)
    motor.set_position(-30)
    time.sleep(1)
    print("done")
    
    
    # initalize for downstroke
    # motor.set_dps(90) # 90 deg/sec
    
    # initalize for upstroke
    #motor.set_power(-50) # Backwards 50%
    # motor.set_dps(-720) # Backwards 720 deg/sec
    
if __name__ == '__main__' :
    try:
        motor.reset_encoder()
        drum_cycle()
        drum_reset_pos()

    except KeyboardInterrupt:
        pass
        """TODO Reset brickpi"""
        reset_brick() # Turn off everything on the brick's hardware, and reset it

    
    
    
    
    
    
    

