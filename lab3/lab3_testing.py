# Testing document for the Mini-Project 1 Robot
# Includes:
#   - One test for the drumming subsystem
#   - One test for the note-production subsystem
#   - One test integrating both subsystems

import time
import unittest
import lab3_drum as drum
import lab3_speaker as speaker
import lab3_triple_input as tripleinput

class SubsystemTest(unittest.TestCase):
    def test_drum(self):
        # Test the drumming subsystem
        drum.drum_init()
        # for f in range(1,4):
        #     drum.drum_cycle(f/2)
        #     # ask the user if the drumming cycle executed well mechanically
        #     if (input(f"Did the drumming cycle execute well mechanically at frequency {f} Hz? (y/n)") == "n"):
        #         self.fail("Drumming cycle failiure at frequency {f} Hz")

        for f in range(1,4):
            thread = drum.start_drum(f/2)
            time.sleep(2)
            drum.stop_drum(thread)
            # ask the user if the drumming loop executed well mechanically
            if (input(f"Did the continuous drumming loop execute with precise timing at frequency {f} Hz? (y/n)") == "n"):
                self.fail("Drumming loop failiure")
        
        # Assert that the drumming subsystem is working correctly
        self.assertEqual(1, 1)

    def test_speaker_range(self):
        # Test the full range of the note-production subsystem
        for n in range (1, 5):
            speaker.play_sound(n)
            time.sleep(1)
        # ask the user if the note played correctly
        if (input("Did all of the notes play correctly? (y/n)") == "n"):
            self.fail("Note failiure")
        
        print(f'Starting user input test')
        while (input("Play a note? (y/n)") == "y"):
            touch_input = tripleinput.collect_input_int()
            if touch_input not in (0,-1):
                print(touch_input)
            speaker.play_sound(touch_input)
            if (input("Did the note play correctly? (y/n)") == "n"):
                self.fail("Note failiure")
        
        # Assert that the note-production subsystem is working correctly
        self.assertEqual(1, 1)
    
class IntegrationTest(unittest.TestCase):
    def test_integration(self):
        # Test the integration of the drumming and note-production subsystems
        drum.drum_init()
        print("test_started")
        thread = None
        for _ in range(30):
            touch_input = tripleinput.collect_input_int()
            if touch_input not in (0,-1):
                print(touch_input)
            speaker.play_sound(touch_input)
            if touch_input == 7:
                thread = drum.start_drum(f/2)
        if thread:
            drum.stop_drum(thread)
        print("done")
        # ask the user if the integration test passed
        if (input("Did the drumming machine and not input integrate well? (y/n)") == "n"):
            self.fail("Integration failiure for drumming machine and note input")
        # Assert that the integration of the drumming and note-production subsystems is working correctly
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()