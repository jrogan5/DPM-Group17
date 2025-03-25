#!/usr/bin/env python3

"""
Main wrapper script for the Firefighter Rescue Robot.
Integrates the ColorDetector and SandbagDispenser classes to detect fires (red stickers)
and deploy sandbags accordingly, using threading for continuous monitoring.

Author: David Vo
Date: March 24, 2025
"""

import os
import csv
import threading
import time
from color_sensor import ColorDetector
from sandbag import SandbagDispenser
from utils.brick import reset_brick

class RobotController:
    """
    Wrapper class to instantiate and manage all physical components of the robot.
    Monitors color detection and triggers sandbag deployment when a fire is detected.
    """
    def __init__(self, color_sensor_port=2, csv_path="./data/color_log.csv"):
        """
        Initializes the robot's components and CSV logging.

        Args:
            color_sensor_port (int): Port for the color sensor (default: 2).
            csv_path (str): Path to the CSV log file (default: "data/color_log.csv").
        """
        # Ensure data directory exists
        if not os.path.exists("data"):
            os.makedirs("data")

        # Initialize components
        self.color_detector = ColorDetector(port=color_sensor_port)
        self.sandbag_dispenser = SandbagDispenser()
        self.csv_path = csv_path
        self.running = False
        self.sandbags_deployed = 0
        self.max_sandbags = 2  # Limit to two sandbags
        self.lock = threading.Lock()  # Thread safety for sandbag deployment

        # Open CSV file for logging
        mode = 'w' if input("Do you want to create a new CSV file? (y/n): ").lower() == 'y' else 'a'
        self.csv_file = open(self.csv_path, mode, newline='')
        if mode == 'w':
            self.csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")
            self.csv_file.flush()

    def start(self):
        """
        Starts the robot's operation by launching the color detection thread.
        """
        self.running = True
        self.color_thread = threading.Thread(target=self._monitor_colors)
        print("Robot started. Monitoring for fires... Press Ctrl+C to stop.")
        self.color_thread.start()
        

    def stop(self):
        """
        Stops the robot's operation and cleans up resources.
        """
        self.running = False
        self.color_thread.join()
        self.csv_file.close()
        reset_brick()
        print("Robot stopped. Brick reset.")

    def _monitor_colors(self):
        """
        Thread function to continuously monitor color detection and trigger sandbag deployment.
        """
        while self.running:
            with self.lock:
                # Log current color detection
                self.color_detector.print_and_log_color(self.csv_file)
                color = self.color_detector.detect_color()

                # Check for red detection and deploy sandbag if conditions met
                if color == "red" and self.sandbags_deployed < self.max_sandbags:
                    print(f"Fire detected! Deploying sandbag #{self.sandbags_deployed + 1}...")
                    self.sandbag_dispenser.deploy_sandbag()
                    self.sandbags_deployed += 1
                    if self.sandbags_deployed == self.max_sandbags:
                        print("All sandbags deployed. Stopping detection.")
                        self.running = False

            time.sleep(0.5)  # Match DELAY_SEC from ColorDetector

    def read_last_color_from_csv(self):
        """
        Reads the last recorded color from the CSV file for verification (optional).

        Returns:
            str: The last detected color ("red", "green", or "none"), or None if file is empty.
        """
        with open(self.csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if len(rows) <= 1:  # Only header or empty
                return None
            return rows[-1][3]  # Color is in the 4th column

if __name__ == "__main__":
    """
    Main execution block to run the robot controller.
    """
    try:
        # Instantiate and start the robot controller
        robot = RobotController()
        robot.start()

        # Keep the main thread alive until interrupted
        while robot.running:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        robot.stop()