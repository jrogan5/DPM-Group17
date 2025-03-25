#!/usr/bin/env python3

"""
Color detection module for the fire-detecting robot.
This module processes RGB data from the EV3 Color Sensor to identify red (fire) or green (obstacles).

Author: David Vo
Date: March 23, 2025
"""

from utils.brick import EV3ColorSensor, wait_ready_sensors, reset_brick
from time import sleep, time
import os
from datetime import datetime
from config import COLOR_SENSOR_PORT

# Constants
DELAY_SEC = 0.5  # Delay between sensor readings for stability

class ColorDetector:
    """
    Class to handle color detection using the EV3 Color Sensor.
    Encapsulates sensor initialization, mode setting, and color detection logic.
    """
    def __init__(self, port=COLOR_SENSOR_PORT, mode="component"):
        """
        Initializes the color detector with the specified port and mode.

        Args:
            port (int): The port number where the sensor is connected (default: 2).
            mode (str): The initial mode for the sensor (default: "component").
        """
        self.sensor = EV3ColorSensor(port, mode=mode)
        wait_ready_sensors(True)  # Block until sensor is ready
        self.mode = mode
        self.port = port
        self.start_time = time()  # Record the start time when the object is created
        self.iteration = 0

    def set_mode(self, mode):
        """
        Sets the sensor to the specified mode.

        Args:
            mode (str): The mode to set (e.g., "component", "ambient", "red", "rawred", "id").
        """
        self.sensor.set_mode(mode)
        wait_ready_sensors(True)
        self.mode = mode

    def detect_color(self):
        """
        Detects the dominant color based on the RGB values from the sensor.
        Requires the sensor to be in "component" mode.

        Returns:
            str: Detected color ("red", "green", or "none").

        Raises:
            ValueError: If the sensor is not in "component" mode.
        """
        if self.mode != "component":
            raise ValueError("Color detection requires 'component' mode.")
        rgb = self.sensor.get_rgb()
        if rgb is None or rgb == [None, None, None]:
            return "none"
        if self.is_red(rgb):
            return "red"
        elif self.is_green(rgb):
            return "green"
        return "none"

    def is_red(self, rgb):
        """
        Determines if the RGB values indicate a red color (potential fire).

        Args:
            rgb (list[float]): List of RGB values [R, G, B].

        Returns:
            bool: True if red is dominant, False otherwise.
        """
        r, g, b = rgb
        return r > 3 * g and r > 4 * b and r > 10

    def is_green(self, rgb):
        """
        Determines if the RGB values indicate a green color (potential obstacle).

        Args:
            rgb (list[float]): List of RGB values [R, G, B].

        Returns:
            bool: True if green is dominant, False otherwise.
        """
        r, g, b = rgb
        return g > 1.2 * r and g > 2 * b and g > 10

    def print_and_log_color(self, csv_file):
        """
        Handles the detected color by printing it to the console and logging it to an open CSV file.
        - Prints a new line for "red" or "green".
        - Prints "none" on the same line using \r and end=" ".
        - Appends the output to the provided CSV file object, including elapsed time since start.

        Args:
            csv_file: An open file object in append mode for logging.
        """
        if self.mode != "component":
            raise ValueError("print_and_log_color requires 'component' mode.")
        color = self.detect_color()
        rgb = self.sensor.get_rgb()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed_time = f"{round(time() - self.start_time, 2):.2f}"  # Time elapsed in seconds, rounded to 2 decimals
        iteration = self.iteration
        self.iteration += 1
        
        if color in ["red", "green"]:
            print(f"{timestamp} - Elapsed: {elapsed_time}s - It: {iteration} - Detected: {color} (RGB: {rgb})")
        else:
            print(f"\r{timestamp} - Elapsed: {elapsed_time}s - It: {iteration} - Detected: none (RGB: {rgb})", end=" ")
        
        # Write to the already open CSV file
        csv_file.write(f"{timestamp},{elapsed_time},{iteration},{color},{rgb[0]},{rgb[1]},{rgb[2]}\n")
        csv_file.flush()  # Ensure data is written to disk immediately

if __name__ == "__main__":
    """
    Debugging mode: Allows user to select sensor mode and test color detection.
    """
    print("Starting color detection debug mode...")
    

    # Ensure data folder exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # Ask user if they want to create a new CSV file
    flush_csv = input("Do you want to create a new CSV file? (y/n): ").lower()
    csv_path = "./data/color_log.csv"
    mode = 'w' if flush_csv == 'y' else 'a'
    print("Hello?")
    # Open the CSV file once at the start
    with open(csv_path, mode) as csv_file:
        # Write header if creating a new file
        if mode == 'w':
            csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")

        # Instantiate the ColorDetector with default port 2
        print("Hello1")
        detector = ColorDetector()
        print("Hello2")
        try:
            while True:
                print("Available modes: c (component mode 'default'), a (ambient), r (red), rr (rawred), i (id)")
                mode_input = input("Enter the sensor mode to test (or 'q' to quit): ").lower()
                if mode_input == 'q':
                    print("Exiting debug mode.")
                    break
                elif mode_input in {"c": "component", "a": "ambient", "r": "red", "rr": "rawred", "i": "id"}:
                    mode = {"c": "component", "a": "ambient", "r": "red", "rr": "rawred", "i": "id"}[mode_input]
                    try:
                        detector.set_mode(mode)
                        print(f"Color sensor initialized in {mode} mode.")
                        print("Detecting colors... Press Ctrl+C to stop.")
                        while True:
                            if mode == "component":
                                detector.print_and_log_color(csv_file)
                            else:
                                value = detector.sensor.get_value()
                                print(f"Value in {mode} mode: {value}")
                            sleep(DELAY_SEC)
                    except KeyboardInterrupt:
                        print("\nStopped by user.")
                    except Exception as e:
                        print(f"Error: {e}")
                        reset_brick()
                        break
                else:
                    print("Invalid mode. Please choose: c (component mode 'default'), a (ambient), r (red), rr (rawred), i (id), or 'q' to quit.")
        except KeyboardInterrupt:
            print("Testing mode interrupted.")
        finally:
            reset_brick()
            print("Brick reset. Exiting program.")