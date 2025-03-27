from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading

SWEEP_MOTOR = Motor("B")
wait_ready_sensors(True)
SWEEP_MOTOR.set_limits(15, 360)
SWEEP_MOTOR.reset_encoder()

def reset_sweep_position(motor: Motor):
    motor.set_position(0)
    time.sleep(2)
    

def sweep(motor: Motor):
    print("motor reset")
    motor.set_position(80)
    time.sleep(3)
    motor.set_position(-80)
    time.sleep(3)
    motor.set_position(0)
    time.sleep(3)
    
    
if __name__ == "__main__":

    sweep(SWEEP_MOTOR)
    while True:
        pass
