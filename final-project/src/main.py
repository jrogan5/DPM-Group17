#!/usr/bin/env python3

"""
Main wrapper script for the Firefighter Rescue Robot.
Integrates ColorDetector, SandbagDispenser, and Siren classes to detect fires,
deploy sandbags, and play a siren, with modular constants and threading.

Author: David Vo, Lucia Cai, James Rogan, Eric Deng
Date: March 28, 2025
"""

import os
import csv
import threading
import time
from color_sensor import ColorDetector, set_csv_path
from sandbag import SandbagDispenser
from siren import Siren
from estop import Estop
from sweeper import Sweeper
from utils.brick import reset_brick, wait_ready_sensors
from config import *
from wheels import Wheels
from odometry import Odometry
from navigation import Navigation

class RobotController:

    def __init__(self):

        try:
            "ESTOP"
            self.estop = Estop()
            
            # "SIREN"
            # use_siren = False
            # self.use_siren = use_siren
            # self.siren = Siren() if self.use_siren else None  
            
            "CSV"
            mode = 'w' 
            self.csv_path = set_csv_path(COLOR_CSV_PATH)
            self.csv_file = open(self.csv_path, mode, newline='')

            if mode == 'w':
                self.csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")
                self.csv_file.flush()

            "COLOR SENSOR"
            self.color_detector = ColorDetector()
            self.cooldown_until = 0
            self.lock = threading.Lock()
            
            "SANDBAG DISPENSER"
            self.sandbag_dispenser = SandbagDispenser()

            "ODOMETRY"
            self.odometry = Odometry()

            "WHEELS"
            # Wheels create child threads for motors, so we don't need to create them here
            self.wheels = Wheels(debug=True, odometry=self.odometry)

            "NAVIGATION"
            self.nav = Navigation(wheels=self.wheels, odometry=self.odometry, debug=True)

            "SWEEPER"
            self.sweeper = Sweeper(debug=True)

            "ROBOT"
            self.running = False

        except Exception as e:
            print(f"Error initializing robot: {e}")

        else:
            print(f"Initializing 'ROBOT CONTROLLER' [{os.path.basename(__file__)}]")

    def start(self):
        print("Robot started!")

        "ROBOT"
        self.running = True

        "ESTOP"
        self.estop_thread = threading.Thread(target=self.estop.start)
        self.estop_thread.start()

        # "SIREN"
        # if self.use_siren:
        #     self.siren_thread = threading.Thread(target=self.siren.start)
        #     self.siren_thread.start()

        "COLOR SENSOR"
        self.color_thread = threading.Thread(target=self._monitor_colors)
        self.color_thread.start()   # detect red: fire extinguish / green: obstacle avoidance

        "ODOMETRY"
        self._start_odometry()
    
    def stop(self):
  
        "ROBOT"
        self.running = False
        
        # "SIREN"
        # if self.use_siren:
        #     self.siren.stop()
        #     self.siren_thread.join()
            
        "COLOR SENSOR"
        self.color_thread.join()
        self.csv_file.close()
        
        "ESTOP"
        self.estop.stop()
        self.estop_thread.join()

        "WHEELS"
        # self.wheels_thread.join()
        
        "RESET"
        reset_brick()
        print("Robot stopped. Brick reset.")

    def _start_odometry(self):
        if self.odometry is None:
            print("odometry not initialized")
            return
        if self.wheels is None:
            print("wheels not initialized")
        print("Wheels and Odometry started!")
        pos = self.odometry.get_xy(self.wheels.direction)
        print(f"(main) Current position: {pos}")
        return pos
        # self.wheels.move_to_coord((pos[0]-20, pos[1]))

    def assume_entry_position(self):
        if START_XY is not None and self.odometry.at_position("N",START_XY):
            print("OK: Assuming entry position.")
            # self.wheels.hard_code_traversal_there()
            self.wheels.move_to_coord((START_XY[0],58))
            self.wheels.move_to_coord((74,58))
            self.wheels.move_to_coord((78,78))
            return True
        else:
            print(f"WARNING: Robot is not at correct START position; adjust the position manually.")
            return False
        
    def assume_exit_position(self):
        if EXIT_XY is not None:
            pos = self.odometry.get_xy(self.wheels.direction)
            print(f"OK: Assuming EXIT position: {EXIT_XY} from current position: {pos}.")
            self.wheels.move_to_coord((EXIT_XY[0], pos[1])) # set the x coordinate
            self.wheels.move_to_coord((EXIT_XY[0], EXIT_XY[1])) # set the y coordinate
            self.wheels.face_direction("S") # set the direction
            if self.odometry.at_position("S", EXIT_XY):
                print("OK: Robot is at correct EXIT position.")
                return True
            else:
                print("WARNING: Robot is not at correct EXIT position; adjust the position manually.")
                return False
        else:
            print("WARNING: EXIT position not set. See config.py.")
            return False
        
    def return_to_start(self):
            if EXIT_XY is not None and self.odometry.at_position("S",EXIT_XY):
                print("OK: Returning to start.")
                self.wheels.move_to_coord((EXIT_XY[0],78))
                self.wheels.move_to_coord((38,78))
                self.wheels.move_to_coord((38,18))
                return True
            else:
                print("WARNING: Robot is not at correct EXIT position; adjust the position manually.")
                return False
            
    def _monitor_colors(self):
        red_count = 0  # Counter for consecutive "red" detections
        green_count = 0

        print("Color sensor started!")
        while self.running:
            current_time = time.time()

            # Skip detection if in cooldown
            if current_time < self.cooldown_until:
                elapsed_time = round(abs(current_time - self.cooldown_until),1)
                print(f"\rCooldown: [{elapsed_time}/{COLOR_COOLDOWN_DURATION}s]", end=" ")
                time.sleep(SENSOR_DELAY)
                continue

            with self.lock:
                self.color_detector.print_and_log_color(self.csv_file)
                color = self.color_detector.detect_color()

                if color == "red":
                    red_count += 1
                    print(f"\rRED DETECTED ({red_count}/{COLOR_RED_CONFIRMATION_COUNT})", end=" ")
                    
                    if red_count >= COLOR_RED_CONFIRMATION_COUNT and self.sandbag_dispenser.sandbags_deployed < MAX_SANDBAGS:
                        print(f"\nFIRE CONFIRMED! Deploying sandbag...")
                        self.sandbag_dispenser.deploy_sandbag()
                        self.cooldown_until = current_time + COLOR_COOLDOWN_DURATION  # Start cooldown
                        red_count = 0  # Reset counter
                        if self.sandbag_dispenser.sandbags_deployed == MAX_SANDBAGS:
                            print("ALL SANDBAGS DEPLOYED. Stopping detection.")
                            self.running = False

                elif color == "green":
                    green_count += 1
                    print(f"\rGREEN DETECTED ({green_count}/{COLOR_GREEN_CONFIRMATION_COUNT})", end=" ")
                    if green_count >= COLOR_GREEN_CONFIRMATION_COUNT:
                        print(f"\nOBSTACLE CONFIMRED! Activating obstacle avoidance...")
                        # TODO: Obstacle Avoidance
                        green_count = 0  # Reset counter
                else:
                    red_count = 0  # Reset if detected
                    green_count = 0

            time.sleep(SENSOR_DELAY)

if __name__ == "__main__":

    try:
        robot = RobotController()
        wait_ready_sensors(True)
        robot.start()
        if not robot.assume_entry_position():
            raise ValueError("Failiure on entry; see above.")
        # robot.nav.navigate_grid()
        time.sleep(5) # test; move the robot to a random position, facing east
        robot.wheels.face_direction("S")
        time.sleep(5)
        if not robot.assume_exit_position():
            raise ValueError("Failure on exit; see above.")
        if not robot.return_to_start():
            raise ValueError("Failiure on return; see above.")
        print("Robot has returned to start position.")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Exception raised: {e}")

    finally:
        robot.stop()
