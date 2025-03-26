"""
This module controls the sandbag deployment mechanism.
It activates the motor to perform a rotation, dispensing a sandbag into a funnel.

Authors: David Vo
Date: March 23, 2025
"""

from utils.brick import Motor, wait_ready_sensors, reset_brick
from config import SANDBAG_MOTOR_PORT, SANDBAG_DEFAULT_DEG, SANDBAG_DEFAULT_DPS, SANDBAG_DEFAULT_POWER
import time
import os

class SandbagDispenser:

    def __init__(self):

        try:
            self.motor = Motor(SANDBAG_MOTOR_PORT)

            self.motor.set_limits(SANDBAG_DEFAULT_POWER, SANDBAG_DEFAULT_DPS)
            self.motor.reset_encoder()
            self.motor.set_position(0)
            self.sandbags_deployed = 0
            
        except Exception as e:
            print(f"Error initializing sandbag dispenser: {e}")

        else:
            print(f"Initializing 'SANDBAG MECHANISM' [{os.path.basename(__file__)}] | Degrees: [{SANDBAG_DEFAULT_DEG} degs] | Degrees per second: [{SANDBAG_DEFAULT_DPS} deg/s] | Power: [{SANDBAG_DEFAULT_POWER} %] | Port: [{SANDBAG_MOTOR_PORT}]")
            

    def deploy_sandbag(self):

        try:
            self.motor.set_position_relative(SANDBAG_DEFAULT_DEG)
            self.sandbags_deployed += 1
            while self.motor.is_moving():
                time.sleep(0.1)
            print(f"SANDBAG DEPLOYED! Total sandbags deployed: [{self.sandbags_deployed}]")
        except Exception as e:
            print(f"Error deploying sandbag: {e}")

if __name__ == "__main__":

    print("TESTING MODE: Sandbag Deployment")

    try:
        dispenser = SandbagDispenser()
        wait_ready_sensors(True)

        print("Entering sandbag deployment testing mode. Waiting for user input...")
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
        print("\nTesting mode interrupted.")
    finally:
        reset_brick()
        print("Brick reset. Exiting program.")
