from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
import color_sensor
import wheels
from wheels import LEFT_WHEEL, RIGHT_WHEEL

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
    time.sleep(2)
    motor.set_position(0)
    time.sleep(2)
    
    
def full_sweep():
    sweep_motor_thread = threading.Thread(target=sweep, args=(SWEEP_MOTOR, ))
    sweep_motor_thread.start()
    detector = color_sensor.ColorDetector()
    color = None
    start_time = time.time()
    while time.time()-start_time < 5:
        color = detector.detect_color()
        print(color)
        if color in ("red, green"):
            break
        time.sleep(0.1)
    if color == "red":
        pos = SWEEP_MOTOR.get_position()
        print(pos)
        sweep_motor_thread.join()
        SWEEP_MOTOR.set_position(pos)
        # Drop block here
        time.sleep(2)
        SWEEP_MOTOR.set_position(0)
    elif color == "green":
        wheels.execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_90")
        wheels.move_forward_1(LEFT_WHEEL, RIGHT_WHEEL)




    
if __name__ == "__main__":
    for i in range(3):
        full_sweep()
        wheels.move_forward_1(LEFT_WHEEL, RIGHT_WHEEL)