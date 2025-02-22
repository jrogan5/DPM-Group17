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
from lab3_emergency_button import emergency_button
from lab3_triple_input import collect_input_int

class SubsystemTest(unittest.TestCase):
    
    def test_button_mapping(self):
        print("Starting button mapping test:")
        print("-"*10)
        for _ in range(5):
            for num in range(1, 8):
                input(f"Press down the buttons in the {num} binary combination, then press Enter")
                if collect_input_int() != num:
                    self.fail("button press was not mapped correctly")
            
        self.assertEqual(1, 1)
    

    def test_estop_latency(self):
        doc = open("test_results/estop_latency_result", "w")
        print("Starting ESTOP latency tests:")
        print("-"*10)
        for test_num in range(1,6):
            input(f"test number {test_num}: Press the estop button as soon as you see a new message appear")
            time.sleep(2)
            print("Press the Estop button!!!")
            t0 = time.time()
            try:
                while time.time()-t0 < 20:
                    emergency_button()
            except KeyboardInterrupt:
                dt = round(time.time()-t0, 2)
                print(f"The button delay was {dt} seconds")
                doc.write(f"{dt}\n")
                self.assertEqual(1, 1)
            doc.close()
            self.fail("Time limit exceeded")

    def test_button_input_latency(self):
        print("Starting triple button latency tests:")
        print("-"*10)
        t0 = time.time()
        doc = open("test_results/triple_button_input_latency", "w")
        for i in range(1, 8):
            input(f"Press the {i} configuration as soon as you see a new message appear")
            time.sleep(1)
            print(f"Press the {i} configuration!!!")
            t0 = time.time()
            while collect_input_int() != i:
                pass
            
            dt = round(time.time()-t0, 2)
            print(f"The button delay was {dt} seconds")
            doc.write(f"{dt}\n")
        doc.close()
        self.fail("Time limit exceeded")
        

    # Sound Subsystem    
    def test_drum(self):
        print("Starting drum SoundTest")
        print("-"*10)
        
        # Test the drumming subsystem
        drum.drum_init()
        for f in range(1,4):
            thread = drum.start_drum(f/2, True)
            time.sleep(10)
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
        print("Integration test started")
        thread = None
        for _ in range(30):
            touch_input = tripleinput.collect_input_int()
            if touch_input not in (0,-1):
                print(touch_input)
            speaker.play_sound(touch_input)
            if touch_input == 7:
                thread = drum.start_drum(1/2, False)
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