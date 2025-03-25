#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, reset_brick

SOUND = sound.Sound(duration=0.3, pitch="A4", volume=100)
TOUCH_SENSOR = TouchSensor(1)


wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound():
    "Play a single note."
    SOUND.play()
    SOUND.wait_done()


def play_sound_on_button_press():
    "In an infinite loop, play a single note when the touch sensor is pressed."
    try:
        while True:
            if TOUCH_SENSOR.is_pressed():
                print("IS PRESSED")
                play_sound()
            while TOUCH_SENSOR.is_pressed(): 
                pass
            
    except BaseException:  # capture all exceptions including KeyboardInterrupt (Ctrl-C)
        print('exiting the program')
        reset_brick()
        exit()


if __name__=='__main__':
    play_sound()

    # TODO Implement this function
    play_sound_on_button_press() 