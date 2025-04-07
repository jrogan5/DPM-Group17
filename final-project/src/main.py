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
from navigation import Navigation

class RobotController:

    def __init__(self):
        self.reduced = True
        try:
            "ESTOP"
            self.estop = Estop()
            
            # "SIREN"
            # use_siren = False
            # self.use_siren = use_siren
            # self.siren = Siren() if self.use_siren else None  
            
            "CSV"
            # mode = 'w' 
            # self.csv_path = set_csv_path(COLOR_CSV_PATH)
            # self.csv_file = open(self.csv_path, mode, newline='')

            # if mode == 'w':
            #     self.csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")
            #     self.csv_file.flush()

            "COLOR SENSOR"
            self.color_detector = ColorDetector()
            # self.cooldown_until = 0
            # self.lock = threading.Lock()
            
            "SANDBAG DISPENSER"
            self.sandbag_dispenser = SandbagDispenser()

            "NAVIGATION"
            self.nav = Navigation(debug=True)
            self.move_threads = None

            "SWEEPER"
            self.sweeper = Sweeper(debug=True)
            self.sweep_thread = None

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

        # "COLOR SENSOR"
        # self.color_thread = threading.Thread(target=self._monitor_colors)
        # self.color_thread.start()   # detect red: fire extinguish / green: obstacle avoidance

    def stop(self):
  
        "ROBOT"
        self.running = False
        
        # "SIREN"
        # if self.use_siren:
        #     self.siren.stop()
        #     self.siren_thread.join()
            
        "COLOR SENSOR"
        # self.color_thread.join()
        # self.csv_file.close()

        "SWEEPER"
        if self.sweep_thread is not None:
            if self.sweep_thread.is_alive():
                self.sweep_thread.join()

        "NAVIGATION"

        
        "ESTOP"
        self.estop.stop()
        self.estop_thread.join()

        "RESET"
        reset_brick()
        print("Robot stopped. Brick reset.")

    def dprint(self,msg:str):
        if self.debug:
            print("(Main) " + msg)

    def hard_sweep_grid(self):
        if ENTRY_XY is None and self.nav.odometry.at_position("N",ENTRY_XY):
            print("WARNING: Robot is not at correct entry position.")
            return False
        if self.reduced:
            self.dprint("Skipping the sweep")
            return True
        self.sweeper.sweeping_on = True
        if self.sweeper.hard_sweep:
            print("(Main) HARD SWEEPING KITCHEN")
            self.nav.wheels.wheels_sweep_init() # reduces the wheel power for slower sweeping
            for dir in self.nav.HARD_SWEEP_PATH:
                self.sweep_thread = self.sweeper.sweep()
                print(f"direction: {dir}")
                time.sleep(3)
                # self.move_threads = self.nav.wheels.move_direction(dir, SWEEP_MOVE)
                # while self.move_threads[0].is_alive():
                #     color = self.color_detector.detect_color()
                #     print(f"Color: {color}")
                #     time.sleep(REFRESH_RATE)
                #     if self.red_detection_routine(color):
                #         self.sweeper.kill_sweep(sweep_thread=self.sweep_thread)
                #         # self.nav.wheels.stop_wheels(forward_move_threads=self.move_threads)
                #         self.sandbag_dispenser.deploy_sandbag()
                #         self.sweeper.reset_sweep_position()
                #         time.sleep(5)
            print("(Main) ending hardcoded sweep routine")
            self.sweeper.sweeping_on = False    
        
        """   # I gave up on this; ultrasonic sensors being bad.        
        else:
            self.sweeper.sweeping_on = True
            self.nav.wheels.wheels_sweep_init() # reduces the wheel power for slower sweeping
            for path_element in self.nav.SWEEP_PATH:
                if path_element == "CCW adjust":
                    print("CCW adjust")
                elif path_element == "CW adjust":
                    print("CW adjust")
                elif path_element == "face south":
                    print("Facing south")
                    self.nav.wheels.face_direction("S")
                    # sweep_thread = self.sweeper.sweep()
                    color = self.color_detector.detect_color()
                    if self.red_detection_routine(color=color):
                        # self.sweeper.kill_sweep()
                        self.nav.wheels.stop_wheels()
                        self.sandbag_dispenser.deploy_sandbag()
                        self.sweeper.reset_sweep_position()
                else:
                    print(f"Path Element: {path_element}")
                    axis,coord = path_element
                    fwd_threads = self.nav.wheels.move_to_coord(axis,coord)
                    # sweep_thread = self.sweeper.sweep()
                    color = self.color_detector.detect_color()
                    if self.red_detection_routine(color=color):
                        # self.sweeper.kill_sweep()
                        self.nav.wheels.stop_wheels()
                        self.sandbag_dispenser.deploy_sandbag()
                        self.sweeper.reset_sweep_position()   
                        self.nav.wheels.move_to_coord(axis,coord) # finish the current move since it was killed prematurely 
        """
        
        self.sweeper.sweeping_on = False
        print("Finished the sweep.")
        return True

    def red_detection_routine(self,color:str):
        if color != "red":
            return False
        self.color_detector.red_count += 1
        print(f"\rRED DETECTED ({self.color_detector.red_count}/{COLOR_RED_CONFIRMATION_COUNT})", end=" ")
        
        if self.color_detector.red_count >= COLOR_RED_CONFIRMATION_COUNT and self.sandbag_dispenser.sandbags_deployed < MAX_SANDBAGS:
            print(f"\nFIRE CONFIRMED! Deploying sandbag...")
            self.cooldown_until = current_time + COLOR_COOLDOWN_DURATION  # Start cooldown
            self.color_detector.red_count = 0  # Reset counter
            if self.sandbag_dispenser.sandbags_deployed == MAX_SANDBAGS:
                print("ALL SANDBAGS DEPLOYED. Stopping detection.")
                return True
        else:
            return False

    def test_system_integration_no_dfs(self):
        if not self.nav.assume_entry_position():
            raise ValueError("Failiure on entry; see above.")
        if not self.hard_sweep_grid():
            raise ValueError("Failiure on sweep; see above.")        
        if self.reduced:
            self.dprint("Reduced version: just facing south and exiting room")
            self.nav.wheels.face_direction("S")
        else:
            if not self.nav.assume_exit_position():
                raise ValueError("Failure on exit; see above.")
        if not self.nav.return_to_start():
            raise ValueError("Failiure on return; see above.")
        print("Robot has returned to start position.")
            
    # I haven't touched this
    def _monitor_colors(self):
        self.color_detector.red_count = 0  # Counter for consecutive "red" detections
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
                    self.color_detector.red_count += 1
                    print(f"\rRED DETECTED ({self.color_detector.red_count}/{COLOR_RED_CONFIRMATION_COUNT})", end=" ")
                    
                    if self.color_detector.red_count >= COLOR_RED_CONFIRMATION_COUNT and self.sandbag_dispenser.sandbags_deployed < MAX_SANDBAGS:
                        print(f"\nFIRE CONFIRMED! Deploying sandbag...")
                        self.sandbag_dispenser.deploy_sandbag()
                        self.cooldown_until = current_time + COLOR_COOLDOWN_DURATION  # Start cooldown
                        self.color_detector.red_count = 0  # Reset counter
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
                    self.color_detector.red_count = 0  # Reset if detected
                    green_count = 0
            time.sleep(SENSOR_DELAY)

if __name__ == "__main__":

    try:
        robot = RobotController()
        wait_ready_sensors(True)
        robot.start()
        robot.test_system_integration_no_dfs()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Exception raised: {e}")

    finally:
        robot.stop()
