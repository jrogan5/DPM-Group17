import lab3_speaker as speaker
import lab3_triple_input as triple_input

if __name__ == "__main__":
    
    while True:
        speaker.play_sound(triple_input.collect_input_int())
        