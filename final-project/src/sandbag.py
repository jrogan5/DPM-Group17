"""
This module controls the sandbag deployment mechanism.
It activates the motor to perform a rotation, dispensing a sandbag into a funnel.

Authors: David Vo
Date: March 23, 2025
"""

from utils.brick import Motor, wait_ready_sensors, reset_brick
from config import SANDBAG_MOTOR_PORT
import time

# Module-level constants for motor control
DEFAULT_DEG = 92    # Degrees to rotate for one sandbag deployment
DEFAULT_DPS = 360   # Degrees per second for motor speed
DEFAULT_POWER = 30  # Power percentage for motor operation

class SandbagDispenser:
    """
    Class to manage the sandbag deployment motor.
    Initializes the motor once and provides a method to deploy sandbags.
    """
    def __init__(self):
        """
        Initializes the sandbag motor with predefined limits and resets its position.
        """
        self.motor = Motor(SANDBAG_MOTOR_PORT)
        self._initialize_motor()
        self.sandbags_deployed = 0

    def _initialize_motor(self):
        """
        Private method to set motor limits, reset encoder, and set initial position.
        """
        try:
            self.motor.set_limits(DEFAULT_POWER, DEFAULT_DPS)
            self.motor.reset_encoder()
            self.motor.set_position(0)
            print("Sandbag motor initialized with {DEFAULT_POWER}% power, {DEFAULT_DPS} DPS.")
        except Exception as e:
            print(f"Error initializing sandbag motor: {e}")

    def deploy_sandbag(self):
        """
        Deploys a single sandbag by rotating the motor by DEFAULT_DEG degrees.
        """
        try:
            self.motor.set_position_relative(DEFAULT_DEG)
            self.sandbags_deployed += 1
            while self.motor.is_moving():
                time.sleep(0.1)
            print(f"Sandbag deployed! Total sandbags deployed: [{self.sandbags_deployed}]")
        except Exception as e:
            print(f"Error deploying sandbag: {e}")

if __name__ == "__main__":
    """
    Testing mode: Allows manual deployment of sandbags when the script is run directly.
    """
    try:
        dispenser = SandbagDispenser()
        print("Entering sandbag deployment testing mode.")
        while True:
            command = input("Enter 'd' to deploy a sandbag, 'q' to quit: ")
            if command == "d":
                dispenser.deploy_sandbag()
            elif command == "q":
                print("Exiting testing mode.")
                break
            else:
                print("Invalid command. Use 'd' or 'q'.")
    except KeyboardInterrupt:
        print("Testing mode interrupted.")
    finally:
        reset_brick()
        print("Brick reset. Exiting program.")
