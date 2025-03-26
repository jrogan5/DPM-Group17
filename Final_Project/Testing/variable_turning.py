#!/usr/bin/env python3

"""
Turning movement based on battery life.
Purpose: preliminary test of using position data to conform to a pre-set path
Hardware Version: V1.1
Date: Maarch 26, 2025
Author: J. Rogan
"""

# Predefined movement values based on different battery levels
BATTERY_THRESHOLDS = {
    "HIGH": 80,
    "MEDIUM": 50,
    "LOW": 20
}

MOVEMENT_MATRIX = {
    "HIGH": {
        "TURN_CCW_90": (200, -200),
        "TURN_CCW_45": (100, -100),
        "TURN_CCW_15": (30, -30),
        "TURN_CW_90": (-200, 200),
        "TURN_CW_45": (-100, 100),
        "TURN_CW_15": (-30, 30)
    },
    "MEDIUM": {
        "TURN_CCW_90": (220, -220),
        "TURN_CCW_45": (110, -110),
        "TURN_CCW_15": (35, -35),
        "TURN_CW_90": (-220, 220),
        "TURN_CW_45": (-110, 110),
        "TURN_CW_15": (-35, 35)
    },
    "LOW": {
        "TURN_CCW_90": (240, -240),
        "TURN_CCW_45": (120, -120),
        "TURN_CCW_15": (40, -40),
        "TURN_CW_90": (-240, 240),
        "TURN_CW_45": (-120, 120),
        "TURN_CW_15": (-40, 40)
    }
}

def get_battery_level(battery_life):
    """Determine battery level category based on percentage."""
    if battery_life >= BATTERY_THRESHOLDS["HIGH"]:
        return "HIGH"
    elif battery_life >= BATTERY_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    else:
        return "LOW"

def execute_turn(left_wheel, right_wheel, movement, battery_life):
    """Executes a predefined turn based on battery life."""
    battery_level = get_battery_level(battery_life)
    if movement in MOVEMENT_MATRIX[battery_level]:
        left_disp, right_disp = MOVEMENT_MATRIX[battery_level][movement]
        left_wheel.set_position_relative(left_disp)
        right_wheel.set_position_relative(right_disp)
        print(f"Executing {movement} with values {left_disp}, {right_disp} at {battery_level} battery level.")
    else:
        print("Invalid movement command.")

# Example usage:
# BATTERY_LIFE = int(input("Enter battery life percentage: "))
# execute_turn(left_wheel, right_wheel, "TURN_CCW_90", BATTERY_LIFE)
