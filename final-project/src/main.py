#!/usr/bin/env python3

"""
Main wrapper script for the Firefighter Rescue Robot.
Integrates ColorDetector, SandbagDispenser, and Siren classes to detect fires,
deploy sandbags, and play a siren, with modular constants and threading.

Author: David Vo
Date: March 24, 2025
"""

import os
import csv
import threading
import time
from color_sensor import ColorDetector, set_csv_path
from sandbag import SandbagDispenser
from siren import Siren
from estop import Estop
from utils.brick import reset_brick, wait_ready_sensors
from config import *

class RobotController:

    def __init__(self):

        try:
            use_siren = True
            self.use_siren = use_siren

            mode = 'w' 
            self.csv_path = set_csv_path(COLOR_CSV_PATH)
            self.csv_file = open(self.csv_path, mode, newline='')

            if mode == 'w':
                self.csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")
                self.csv_file.flush()

            # Initialize components
            self.color_detector = ColorDetector()
            self.sandbag_dispenser = SandbagDispenser()
            self.siren = Siren() if self.use_siren else None  # Only instantiate if siren is enabled
            self.estop = Estop()
            
            self.running = False
            self.sandbags_deployed = 0
            self.lock = threading.Lock()
            self.cooldown_until = 0  # Timestamp when cooldown ends

        except Exception as e:
            print(f"Error initializing robot: {e}")

        else:
            print(f"Initializing 'ROBOT CONTROLLER' [{os.path.basename(__file__)}]")

        
    def start(self):
        print("Robot started! Monitoring for fires... Press Ctrl+C to stop.")
        self.running = True

        if self.use_siren:
            self.siren_thread = threading.Thread(target=self.siren.start)
            self.siren_thread.start()

        self.color_thread = threading.Thread(target=self._monitor_colors)
        self.color_thread.start()   # detect red: fire extinguish / green: obstacle avoidance

        # TODO: Navigation to Kitchen
        # TODO: Sweeping


        
        

    def stop(self):
  
        self.running = False
        if self.use_siren:
            self.siren.stop()
            self.siren_thread.join()
        self.color_thread.join()
        self.csv_file.close()
        reset_brick()
        print("Robot stopped. Brick reset.")

    def _monitor_colors(self):
        red_count = 0  # Counter for consecutive "red" detections
        green_count = 0

        while self.running:
            current_time = time.time()

            # Skip detection if in cooldown
            if current_time < self.cooldown_until:
                elapsed_time = round(abs(current_time - self.cooldown_until),1)
                print(f"\rCooldown: [{elapsed_time}/{COLOR_COOLDOWN_DURATION}s]", end=" ")
                time.sleep(COLOR_SENSOR_DELAY)
                continue

            with self.lock:
                self.color_detector.print_and_log_color(self.csv_file)
                color = self.color_detector.detect_color()

                if color == "red":
                    red_count += 1
                    print(f"\rRED DETECTED ({red_count}/{COLOR_RED_CONFIRMATION_COUNT})", end=" ")
                    # TODO: Halt all robot movements here (not implemented yet)
                    # TODO: Move robot back to deposit sandbag (not implemented yet)
                    if red_count >= COLOR_RED_CONFIRMATION_COUNT and self.sandbags_deployed < MAX_SANDBAGS:
                        print(f"\nFIRE CONFIRMED! Deploying sandbag...")
                        self.sandbag_dispenser.deploy_sandbag()
                        self.sandbags_deployed += 1
                        self.cooldown_until = current_time + COLOR_COOLDOWN_DURATION  # Start cooldown
                        red_count = 0  # Reset counter
                        if self.sandbags_deployed == MAX_SANDBAGS:
                            print("ALL SANDBAGS DEPLOYED. Stopping detection.")
                            self.running = False

                if color == "green":
                    green_count += 1
                    print(f"\rGREEN DETECTED ({green_count}/{COLOR_GREEN_CONFIRMATION_COUNT})", end=" ")
                    if green_count >= COLOR_GREEN_CONFIRMATION_COUNT:
                        print(f"\nOBSTACLE CONFIMRED! Activating obstacle avoidance...")
                        # TODO: Obstacle Avoidance
                        green_count = 0  # Reset counter
                else:
                    red_count = 0  # Reset if detected
                    green_count = 0

            time.sleep(COLOR_SENSOR_DELAY)

    def read_last_color_from_csv(self):

        with open(self.csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) <= 1:
                return None
            return rows[-1][3]








if __name__ == "__main__":

    try:
        robot = RobotController()
        wait_ready_sensors(True)
        time.sleep(2)
        robot.start()

        while robot.running:
            robot.estop.check_stop()    # checks for estop
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        robot.stop()