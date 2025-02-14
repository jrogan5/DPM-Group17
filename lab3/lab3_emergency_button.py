''' lab3_emergency_button
Performs the emergency stop function when pressed.
Stops all ongoing processes.

Authors: David Vo, Eric Deng
February 14th, 2025
'''

from utils.brick import TouchSensor, reset_brick, wait_ready_sensors
import lab3_drum as drum
import time

BUTTON = TouchSensor(4)

wait_ready_sensors(True)

def emergency_button():
    "stops everything when pressed, stops drum thread"
    if BUTTON.is_pressed():
        print("EMERGENCY BUTTON PRESSED")
        raise KeyboardInterrupt
        print("Stopped")
        