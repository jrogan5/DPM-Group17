from utils.brick import Motor, wait_ready_sensors, reset_brick
import time
import threading
import color_sensor
import wheels
from wheels import LEFT_WHEEL, RIGHT_WHEEL
import sandbag
import ctypes

SWEEP_MOTOR = Motor("B")
wait_ready_sensors(True)
SWEEP_MOTOR.set_limits(15, 360)
SWEEP_MOTOR.reset_encoder()
SANDBAG = sandbag.SandbagDispenser()

def reset_sweep_position(motor: Motor):
    motor.set_position(0)
    time.sleep(2)

def sweep(motor: Motor):
    try:
        reset_sweep_position(motor)
        motor.set_position(160)
        time.sleep(2)
        motor.set_position(0)
        time.sleep(2)
    except RuntimeError:
        print("Thread ended forcibly")


def force_kill_thread(thread, exception_type):
    """Inject an exception into a running thread."""
    tid = thread.ident
    if tid is None:
        raise ValueError("Thread has not started or has already finished.")
    
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exception_type)
    )
    
    if res > 1:  # If more than one thread was affected, reset it
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed.")
    
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
        force_kill_thread(sweep_motor_thread, RuntimeError)
        SWEEP_MOTOR.set_position(pos)
        time.sleep(1)
        SANDBAG.deploy_sandbag()
        time.sleep(2)
        SWEEP_MOTOR.set_position(0)
    elif color == "green":
        wheels.execute_turn(LEFT_WHEEL, RIGHT_WHEEL, "CW_90")
        time.sleep(2)
        wheels.move_forward_1(LEFT_WHEEL, RIGHT_WHEEL)
        time.sleep(2)




    
if __name__ == "__main__":
    for i in range(3):
        full_sweep()
        wheels.forward_move(70, LEFT_WHEEL, RIGHT_WHEEL)