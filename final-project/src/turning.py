#!/usr/bin/env python3

"""
Turning movement based on battery life.
Purpose: preliminary test of using position data to conform to a pre-set path
Hardware Version: V1.1
Date: Maarch 26, 2025
Author: J. Rogan
"""

BIG = 192
MED = BIG/2
SML = BIG/4
RW_ADJ = -3 # Right wheel adjustment
CCW_ADJ = 5

MOVEMENT_MATRIX = {
    "CCW_90": (BIG+CCW_ADJ, -(BIG+CCW_ADJ)),
    "CCW_45": (MED+CCW_ADJ, -(MED+CCW_ADJ)),
    "CCW_15": (SML+CCW_ADJ, -(SML+CCW_ADJ)),
    "CW_90": (-BIG, BIG),
    "CW_45": (-MED, MED),
    "CW_15": (-SML, SML)
}


def execute_turn(left_wheel, right_wheel, movement):
    """Executes a predefined turn based on battery life."""
    if movement in MOVEMENT_MATRIX:
        left_disp, right_disp = MOVEMENT_MATRIX[movement]
        left_wheel.set_position_relative(left_disp)
        right_wheel.set_position_relative(right_disp)
        print(f"Executing {movement} with values {left_disp}, {right_disp}. ")
    else:
        print("Invalid movement command.")

# Example usage:
# BATTERY_LIFE = int(input("Enter battery life percentage: "))
# execute_turn(left_wheel, right_wheel, "TURN_CCW_90", BATTERY_LIFE)