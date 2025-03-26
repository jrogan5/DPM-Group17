#!/usr/bin/env python3

"""
Siren module for the Firefighter Rescue Robot.
Plays a continuous two-note siren sound using the speaker.

Authors: David Vo, James Rogan, Brian Morava (original lab3_speaker)
Modified by: [Your Name]
Date: March 24, 2025
"""

from utils import sound
import time
import os
from config import SIREN_DURATION, SIREN_NOTE_DURATION, SIREN_VOLUME
class Siren:

    def __init__(self):

        # Define two notes for the siren (e.g., C4 and C5)
        self.note1 = sound.Sound(duration=SIREN_NOTE_DURATION, pitch="C4", volume=SIREN_VOLUME)  # Lower octave
        self.note2 = sound.Sound(duration=SIREN_NOTE_DURATION, pitch="C5", volume=SIREN_VOLUME)  # Higher octave
        self.running = False
        print(f"Initializing 'SIREN' [{os.path.basename(__file__)}] | Note1: [{self.note1.pitch}, {self.note1.volume}% volume] | Note2: [{self.note2.pitch}, {self.note2.volume}% volume] | Duration: [{SIREN_DURATION}s]")

    def start(self):

        self.running = True
        print("Siren started.")
        while self.running:
            self.note1.play()
            time.sleep(SIREN_DURATION)  # Duration of note1
            if not self.running:
                break
            self.note2.play()
            time.sleep(SIREN_DURATION)  # Duration of note2

    def stop(self):

        self.running = False
        print("Siren stopped.")

if __name__ == "__main__":

    print("TESTING MODE: Siren")

    try:
        siren = Siren()
        siren.start()
    except KeyboardInterrupt:
        siren.stop()
        print("Test interrupted.")