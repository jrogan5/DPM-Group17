#!/usr/bin/env python4
import time
from utils.sound import Sound, Song, NOTES

def main():
    # Melody from "Fly Me to the Moon" with octaves (82 notes)
    melody_with_octave = [
        # Verse: "Fly me to the moon..."
        'C5', 'B4', 'A4', 'G4', 'F4', 'G4', 'A4', 'C5',  # "Fly me to the moon"
        'B4', 'A4', 'G4', 'F4', 'E4', 'A4', 'G4', 'F4',   # "Let me play among"
        'E4', 'D4', 'E4', 'F4', 'A4', 'G#4', 'F4', 'E4',  # "the stars, Let me"
        'D4', 'C4', 'C#4', 'D4', 'A4', 'A4', 'C5', 'B4',  # "see what spring is like"
        'G4', 'B4', 'C5', 'F5', 'F5', 'A5', 'G5', 'F5',   # "On a-Jupiter and Mars"
        'E5', 'C5', 'B4', 'A4', 'G4', 'F4', 'G4', 'A4',   # "In other words, hold my"
        
        # Repeat with variation: "Fill my heart with song..."
        'C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'A4', 'G4',   # "Fill my heart with song"
        'F4', 'E4', 'D4', 'E4', 'F4', 'A4', 'G#4', 'F4',  # "And let me sing forever"
        'E4', 'D4', 'C4', 'C#4', 'D4', 'A4', 'A4', 'C5',  # "more, You are all I long"
        'B4', 'G4', 'G#4', 'A4', 'C5', 'C5', 'C5', 'D5',  # "for, all I worship and"
        'C5', 'G4', 'D5', 'C5'                                  # "adore"
    ]

    # Verify length matches original
    assert len(melody_with_octave) == 84, f"Expected 84 notes, got {len(melody_with_octave)}"

    # Create a Song object
    song = Song()

    # Add each note as a Sound object with a fixed duration
    note_duration = 0.5  # Quarter note duration in seconds (adjustable for tempo)
    for note in melody_with_octave:
        sound = Sound(duration=note_duration, pitch=note, volume=80)  # 50% volume
        song.append(sound)

    # Compile the song
    print("Compiling song...")
    song.compile()
    print(f"Song duration: {song.duration} seconds")

    # Play the song
    print("Playing 'Fly Me to the Moon'...")
    song.play()

    # Wait for the song to finish
    song.sleep_done()  # Or use song.wait_done() for a more precise wait
    song.stop()
    print("Song finished.")

if __name__ == "__main__":
    main()