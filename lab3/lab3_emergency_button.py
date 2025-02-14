from utils.brick import TouchSensor, reset_brick, wait_ready_sensors
import lab3_drum as drum
import time

BUTTON = TouchSensor(4)

wait_ready_sensors(True)

def emergency_button():
    if BUTTON.is_pressed():
        print("EMERGENCY BUTTON PRESSED")
        drum.stop_drum()
        reset_brick()
        exit()
        