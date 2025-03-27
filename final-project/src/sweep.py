from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
import color_sensor

SWEEP_MOTOR = Motor("B")
wait_ready_sensors(True)
SWEEP_MOTOR.set_limits(15, 360)
SWEEP_MOTOR.reset_encoder()

def reset_sweep_position(motor: Motor):
    motor.set_position(0)
    time.sleep(2)

def sweep(motor: Motor):
    reset_sweep_position(motor)
    motor.set_position(160)
    time.sleep(3)
    motor.set_position(0)
    time.sleep(3)
    
    
if __name__ == "__main__":
    sweep_motor_thread = threading.Thread(target=sweep, args=(SWEEP_MOTOR, ))
    sweep_motor_thread.start()
    detector = color_sensor.ColorDetector()
    color = None
    while color != "red":
        color = detector.detect_color()
        print(color)
        time.sleep(0.1)
    pos = SWEEP_MOTOR.get_position()
    print(pos)
    sweep_motor_thread.join()
    print(pos)
    time.sleep(2)
    SWEEP_MOTOR.set_position(pos)
    # Drop block here
    time.sleep(5)
    SWEEP_MOTOR.set_position(0)