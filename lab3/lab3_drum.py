'''
Controls the drumming mechanism 
'''

from utils.brick import Motor
import time
other_motor = Motor("C")

motor = Motor("A")

def drum_reset_pos() :
    this.set_position(720)
    time.sleep(2) # Wait to finish

def drum_cycle() :
    
    # initalize for downstroke
    motor.set_power(100) # 100%
    # motor.set_dps(90) # 90 deg/sec
    
    # initalize for upstroke
    #motor.set_power(-50) # Backwards 50%
    # motor.set_dps(-720) # Backwards 720 deg/sec
    
if __name__ == '__main__' :
    motor.drum_reset_pos()
    
    
    
    
    
    
    
    

