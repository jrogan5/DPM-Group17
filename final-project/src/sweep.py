from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
import color_sensor

SWEEP_MOTOR = Motor("B")
wait_ready_sensors(True)
SWEEP_MOTOR.set_limits(30, 360)


def reset_sweep_position(motor: Motor):
    motor.set_position(0)
    

def sweep(motor: Motor):
    reset_sweep_position(motor)
    motor.set_position(100)
    motor.get_position
    
    
if __name__ == "__main__":
    sweep_motor_thread = threading.Thread(target=sweep, args=(SWEEP_MOTOR))
    detector = color_sensor.ColorDetector()
    for i in range(20):
        color = detector.detect_color()
        print(color)
    
    