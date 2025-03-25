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

class Siren:
    """
    Class to manage a continuous two-note siren sound.
    Plays alternating notes at different octaves in a loop.
    """
    def __init__(self):
        """
        Initializes the siren with two notes at different octaves.
        """
        # Define two notes for the siren (e.g., C4 and C5)
        self.note1 = sound.Sound(duration=0.5, pitch="C4", volume=80)  # Lower octave
        self.note2 = sound.Sound(duration=0.5, pitch="C5", volume=80)  # Higher octave
        self.running = False

    def start(self):
        """
        Starts playing the siren in a continuous loop.
        """
        self.running = True
        print("Siren started.")
        while self.running:
            self.note1.play()
            time.sleep(0.5)  # Duration of note1
            if not self.running:
                break
            self.note2.play()
            time.sleep(0.5)  # Duration of note2

    def stop(self):
        """
        Stops the siren playback.
        """
        self.running = False
        print("Siren stopped.")

if __name__ == "__main__":
    """
    Testing mode: Plays the siren until interrupted.
    """
    try:
        siren = Siren()
        siren.start()
    except KeyboardInterrupt:
        siren.stop()
        print("Test interrupted.")