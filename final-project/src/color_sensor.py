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
from config import COLOR_SENSOR_PORT, COLOR_SENSOR_DELAY, COLOR_CSV_PATH

def set_csv_path(color_csv_path=COLOR_CSV_PATH):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, "src", "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    csv_path = os.path.join(project_root, color_csv_path)
    return csv_path

class ColorDetector:

    def __init__(self):

        try: 
            self.sensor = EV3ColorSensor(COLOR_SENSOR_PORT)

            self.start_time = time()  
            self.iteration = 0
            self.csv_path = set_csv_path()

        except Exception as e:
            print(f"Error initializing color sensor: {e}")

        else:
            print(f"Initializing 'COLOR SENSOR' [{os.path.basename(__file__)}] | Delay: [{COLOR_SENSOR_DELAY}s] | CSV: [{COLOR_CSV_PATH}] | Port: [{COLOR_SENSOR_PORT}]")

    def detect_color(self):

        rgb = self.sensor.get_rgb()
        if rgb is None or rgb == [None, None, None]:
            return "none"
        if self.is_red(rgb):
            return "red"
        elif self.is_green(rgb):
            return "green"
        return "none"

    def is_red(self, rgb):

        r, g, b = rgb
        return r > 2.5 * g and r > 2.5 * b and r > 10

    def is_green(self, rgb):

        r, g, b = rgb
        return g > 0.8 * r and g > 2 * b and g > 10

    def print_and_log_color(self, csv_file):

        color = self.detect_color()
        rgb = self.sensor.get_rgb()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elapsed_time = f"{round(time() - self.start_time, 2):.2f}"  # Time elapsed in seconds, rounded to 2 decimals
        iteration = self.iteration
        self.iteration += 1
        
        if color in ["red", "green"]:
            print(f"\r{timestamp} - Elapsed: {elapsed_time}s - It: {iteration} - Color: {color} (RGB: {rgb})")
        else:
            print(f"\r{timestamp} - Elapsed: {elapsed_time}s - It: {iteration} - Color: none (RGB: {rgb})", end=" ")
        
        # Write to the already open CSV file
        csv_file.write(f"{timestamp},{elapsed_time},{iteration},{color},{rgb[0]},{rgb[1]},{rgb[2]}\n")
        csv_file.flush()  # Ensure data is written to disk immediately

if __name__ == "__main__":

    try:
        print("TESTING MODE: Color Sensor")
        detector = ColorDetector()
        wait_ready_sensors(True)

        csv_path = detector.csv_path
        flush_csv = input("Do you want to create a new CSV file? (y/n): ").lower()
        mode = 'w' if flush_csv == 'y' else 'a'

        # Open the CSV file once at the start
        with open(csv_path, mode) as csv_file:
            # Write header if creating a new file
            if mode == 'w':
                csv_file.write("timestamp,elapsed_time,iteration,color,R,G,B\n")
            
            try:
                ("Detecting colors... Press Ctrl+C to stop.")
                while True:  
                    detector.print_and_log_color(csv_file)
                    sleep(COLOR_SENSOR_DELAY)

            except KeyboardInterrupt:
                print("\nTesting mode interrupted.")
            

    except KeyboardInterrupt:
        print("\nTesting mode interrupted.")

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        reset_brick()
        print("Brick reset. Exiting program.")
