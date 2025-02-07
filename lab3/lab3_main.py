import lab3_speaker as speaker
import lab3_triple_input as triple_input
from lab3_emergency_button import emergency_button
import lab3_drum as drum

if __name__ == "__main__":
    drum.drum_init()
    drum_started = False
    while True:
        touch_input = triple_input.collect_input_int()
        print(touch_input)
        speaker.play_sound(touch_input)
        emergency_button()
        if touch_input == 7:
            drum_started = True

        if drum_started:
            drum.drum_cycle()
        