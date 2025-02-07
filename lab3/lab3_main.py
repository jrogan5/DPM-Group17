import lab3_speaker as speaker
import lab3_triple_input as triple_input
from lab3_emergency_button import emergency_button

if __name__ == "__main__":
    
    while True:
        speaker.play_sound(triple_input.collect_input_int())
        emergency_button()
        