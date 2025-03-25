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
from color_sensor import ColorDetector
from sandbag import SandbagDispenser
from siren import Siren
from utils.brick import reset_brick
from config import COLOR_SENSOR_PORT, SANDBAG_MOTOR_PORT

# Modular constants
DELAY_SEC = 0.5              # Delay between sensor readings (seconds)
RED_CONFIRMATION_COUNT = 10  # Number of consecutive "red" detections to confirm a fire
COOLDOWN_DURATION = 10.0     # Cooldown period after sandbag deployment (seconds)
MAX_SANDBAGS = 2             # Maximum number of sandbags to deploy
CSV_PATH = "src/data/color_log.csv"  # Hardcoded CSV path

class RobotController:
    """
    Wrapper class to manage robot components: color detection, sandbag deployment, and siren.
    Monitors colors with fire confirmation logic and runs the siren as an optional thread.
    """
    def __init__(self, color_sensor_port=COLOR_SENSOR_PORT, use_siren=False):
        """
        Initializes the robot's components and CSV logging.

        Args:
            color_sensor_port (int): Port for the color sensor.
            use_siren (bool): Whether to activate the siren (default: True).
        """
        # Get project root and set data directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        data_dir = os.path.join(project_root, "src", "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.csv_path = os.path.join(project_root, CSV_PATH)

        # Initialize components
        self.color_detector = ColorDetector(port=color_sensor_port)
        self.sandbag_dispenser = SandbagDispenser()
        self.siren = Siren() if use_siren else None  # Only instantiate if siren is enabled
        self.use_siren = use_siren
        self.running = False
        self.sandbags_deployed = 0
        self.lock = threading.Lock()
        self.cooldown_until = 0  # Timestamp when cooldown ends

        # Open CSV file for logging
        mode = 'w' if input("Do you want to create a new CSV file? (y/n): ").lower() == 'y' else 'a'
        self.csv_file = open(self.csv_path, mode, newline='')
        if mode == 'w':
            self.csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")
            self.csv_file.flush()

    def start(self):
        """
        Starts the robot's operation with color detection and optional siren threads.
        """
        self.running = True
        self.color_thread = threading.Thread(target=self._monitor_colors)
        self.color_thread.start()
        if self.use_siren:
            self.siren_thread = threading.Thread(target=self.siren.start)
            self.siren_thread.start()
        print("Robot started. Monitoring for fires... Press Ctrl+C to stop.")

    def stop(self):
        """
        Stops the robot's operation and cleans up resources.
        """
        self.running = False
        if self.use_siren:
            self.siren.stop()
            self.siren_thread.join()
        self.color_thread.join()
        self.csv_file.close()
        reset_brick()
        print("Robot stopped. Brick reset.")

    def _monitor_colors(self):
        """
        Thread function to monitor color detection with fire confirmation and cooldown.
        """
        red_count = 0  # Counter for consecutive "red" detections
        while self.running:
            current_time = time.time()

            # Skip detection if in cooldown
            if current_time < self.cooldown_until:
                print(f"\rColor sensor on cooldown until {self.cooldown_until:.2f}...", end=" ")
                time.sleep(DELAY_SEC)
                continue

            with self.lock:
                self.color_detector.print_and_log_color(self.csv_file)
                color = self.color_detector.detect_color()

                if color == "red":
                    red_count += 1
                    print(f"\rRed detected ({red_count}/{RED_CONFIRMATION_COUNT})", end=" ")
                    # TODO: Halt all robot movements here (not implemented yet)
                    if red_count >= RED_CONFIRMATION_COUNT and self.sandbags_deployed < MAX_SANDBAGS:
                        print(f"\nFire confirmed! Deploying sandbag #{self.sandbags_deployed + 1}...")
                        self.sandbag_dispenser.deploy_sandbag()
                        self.sandbags_deployed += 1
                        self.cooldown_until = current_time + COOLDOWN_DURATION  # Start cooldown
                        red_count = 0  # Reset counter
                        if self.sandbags_deployed == MAX_SANDBAGS:
                            print("All sandbags deployed. Stopping detection.")
                            self.running = False
                else:
                    red_count = 0  # Reset if non-red detected

            time.sleep(DELAY_SEC)

    def read_last_color_from_csv(self):
        """
        Reads the last recorded color from the CSV file for verification (optional).

        Returns:
            str: The last detected color ("red", "green", or "none"), or None if file is empty.
        """
        with open(self.csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) <= 1:
                return None
            return rows[-1][3]

if __name__ == "__main__":
    """
    Main execution block to run the robot controller.
    """
    try:
        # Ask user if they want the siren
        use_siren = input("Do you want the siren to play? (y/n): ").lower() == 'y'
        robot = RobotController(use_siren=use_siren)
        robot.start()
        while robot.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        robot.stop()