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

RW_ADJ = -3 # Right wheel adjustment
CCW_ADJ = 5
BAT_34_ADJ = 0 # Battery 34 adjustment

MOVEMENT_MATRIX = {
    "BAT_33": {
    "CCW_90": (BIG+CCW_ADJ, -(BIG+CCW_ADJ)),
    "CCW_45": (MED+CCW_ADJ, -(MED+CCW_ADJ)),
    "CCW_15": (SML+CCW_ADJ, -(SML+CCW_ADJ)),
    "CW_90": (-BIG, BIG),
    "CW_45": (-MED, MED),
    "CW_15": (-SML, SML)
    },
    "BAT_34": {
    "CCW_90": (BIG+CCW_ADJ + BAT_34_ADJ, -(BIG+CCW_ADJ + BAT_34_ADJ)),
    "CCW_45": (MED+CCW_ADJ+BAT_34_ADJ, -(MED+CCW_ADJ+BAT_34_ADJ)),
    "CCW_15": (SML+CCW_ADJ+BAT_34_ADJ, -(SML+CCW_ADJ+BAT_34_ADJ)),
    "CW_90": (-(BIG+BAT_34_ADJ), BIG+BAT_34_ADJ),
    "CW_45": (-(MED+BAT_34_ADJ), MED+BAT_34_ADJ),
    "CW_15": (-(SML+BAT_34_ADJ), SML)
    }
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
