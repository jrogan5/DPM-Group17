import lab3_speaker as speaker
import lab3_triple_input as triple_input
from utils.brick import Motor, wait_ready_sensors, reset_brick
from lab3_emergency_button import emergency_button
import lab3_drum as drum

if __name__ == "__main__":
    drum.drum_init()

    try:
        while True:
            touch_input = triple_input.collect_input_int()
            if touch_input not in (0,-1):
                print(f"Touch Input: {touch_input}")
            speaker.play_sound(touch_input)
            emergency_button()
            if touch_input == 7:
                print(f"Starting Drum!")
                drum.start_drum()

    except KeyboardInterrupt:
        drum.stop_drum()
        reset_brick()

        
        