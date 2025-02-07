#!/usr/bin/env python3

"""
Module to play sounds when the touch sensor is pressed.
This file must be run on the robot.
"""
 
from utils import sound
from utils.brick import TouchSensor, wait_ready_sensors, reset_brick
import time

C4 = sound.Sound(duration=0.3, pitch="C4", volume=100)
D4 = sound.Sound(duration=0.3, pitch="D4", volume=100)
E4 = sound.Sound(duration=0.3, pitch="E4", volume=100)
F4 = sound.Sound(duration=0.3, pitch="F4", volume=100)
G4 = sound.Sound(duration=0.3, pitch="G4", volume=100)
A5 = sound.Sound(duration=0.3, pitch="A5", volume=100)
B5 = sound.Sound(duration=0.3, pitch="B5", volume=100)
C5 = sound.Sound(duration=0.3, pitch="C5", volume=100)
D5 = sound.Sound(duration=0.3, pitch="D5", volume=100)
E5 = sound.Sound(duration=0.3, pitch="E5", volume=100)
F5 = sound.Sound(duration=0.3, pitch="F5", volume=100)
G5 = sound.Sound(duration=0.3, pitch="G5", volume=100)
A6 = sound.Sound(duration=0.3, pitch="A6", volume=100)
B6 = sound.Sound(duration=0.3, pitch="B6", volume=100)



wait_ready_sensors() # Note: Touch sensors actually have no initialization time

mary_had_a_little_lab = [E4,D4,C4,D4,E4,E4, E4, E4, D4, D4, D4, D4, E4, G4, G4, G4, E4,D4,C4,D4,E4,E4, E4, E4, D4, D4, E4,D4,C4, C4, C4, C4]

def play_sound(x):
    if x==1:
        C4.play()
    elif x==2:
        E4.play()
    elif x==3:
        C5.play()
    elif x==4:
        G4.play()
        
def play_song(array):
    for note in array:
        note.play()
        time.sleep(1)

if __name__=='__main__':
    play_song(mary_had_a_little_lab)
   # while(1):
    #    x = input("enter note # (1,2,3,4): ")
     #   play_sound(int(x))
        
