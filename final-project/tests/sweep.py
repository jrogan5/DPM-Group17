from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading

SWEEP_MOTOR = Motor("B")
wait_ready_sensors(True)
SWEEP_MOTOR.set_limits(30, 360)


def reset_sweep_position(motor: Motor):
    motor.set_position(0)
    

def sweep(motor: Motor):
    reset_sweep_position()
    motor.set_position(100)
    
    
if __name__ == "__main__":
    sweep(SWEEP_MOTOR)