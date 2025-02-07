#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, reset_brick

C4 = sound.Sound(duration=0.3, pitch="C4", volume=100)
E4 = sound.Sound(duration=0.3, pitch="E4", volume=100)
G4 = sound.Sound(duration=0.3, pitch="G4", volume=100)
B4 = sound.Sound(duration=0.3, pitch="B4", volume=100)

wait_ready_sensors() # Note: Touch sensors actually have no initialization time


def play_sound(x):
    if x==1:
        C4.play()
    elif x==2:
        E4.play()
    elif x==4:
        G4.play()
    elif x==3:
        B4.play()

if __name__=='__main__':
    
    while(1):
        x = input("enter note # (1,2,3,4): ")
        play_sound(int(x))
        
