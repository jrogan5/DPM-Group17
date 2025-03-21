

#!/usr/bin/env python3

"""
Color detection module for the fire-detecting robot.
This module processes RGB data from the EV3 Color Sensor to identify red (fire) or green (obstacles).

Author: David Vo
Date: March 21, 2025
"""

from utils.brick import EV3ColorSensor, wait_ready_sensors, reset_brick
from time import sleep

# Constants
DELAY_SEC = 0.05  # Delay between sensor readings for stability
COLOR_SENSOR_PORT = 2  # Port where the color sensor is connected

def detect_color(sensor: EV3ColorSensor) -> str:
    """
    Detects the dominant color using the EV3ColorSensor's RGB values.
    
    Args:
        sensor (EV3ColorSensor): The initialized color sensor object.
    
    Returns:
        str: Detected color ("red", "green", or "none").
    """
    rgb = sensor.get_rgb()
    if rgb is None or rgb == [None, None, None]:
        return "none"
    
    if is_red(rgb):
        return "red"
    elif is_green(rgb):
        return "green"
    return "none"

def is_red(rgb: list[float]) -> bool:
    """
    Determines if the RGB values indicate a red color (potential fire).
    
    Args:
        rgb (list[float]): List of RGB values [R, G, B].
    
    Returns:
        bool: True if red is dominant, False otherwise.
    """
    r, g, b = rgb
    return r > 3 * g and r > 4 * b and r > 10 # Threshold for red detection

def is_green(rgb: list[float]) -> bool:
    """
    Determines if the RGB values indicate a green color (potential obstacle).
    
    Args:
        rgb (list[float]): List of RGB values [R, G, B].
    
    Returns:
        bool: True if green is dominant, False otherwise.
    """
    r, g, b = rgb
    return g > 1.2 * r and g > 2 * b and g > 10  # Threshold for green detection

def initialize_sensor(port: int = COLOR_SENSOR_PORT, mode: str = "component") -> EV3ColorSensor:
    """
    Initializes the EV3 Color Sensor on the specified port with the given mode.
    
    Args:
        port (int): The port number where the sensor is connected (default: 2).
        mode (str): The mode for the sensor (default: "component").
    
    Returns:
        EV3ColorSensor: Initialized sensor object.
    """
    sensor = EV3ColorSensor(port, mode=mode)
    wait_ready_sensors(True)  # Block until sensor is ready
    return sensor

if __name__ == "__main__":
    """
    Debugging mode: Allows user to select sensor mode and test color detection.
    """
    print("Starting color detection debug mode...")
    print("Available modes: component (RGB), ambient, red, rawred, id")

    # Get user input for sensor mode
    while True:
        mode = input("Enter the sensor mode to test (or 'q' to quit): ").lower()
        if mode == 'q':
            print("Exiting debug mode.")
            break
        elif mode in ["component", "ambient", "red", "rawred", "id"]:
            try:
                # Initialize sensor with selected mode
                color_sensor = initialize_sensor(COLOR_SENSOR_PORT, mode)
                print(f"Color sensor initialized in {mode} mode.")
                
                # Run detection loop
                print("Detecting colors... Press Ctrl+C to stop.")
                while True:
                    if mode == "component":
                        rgb = color_sensor.get_rgb()
                        color = detect_color(color_sensor)
                        #if color != "none":
                        print(f"RGB: {rgb}, Detected: {color}")
                    else:
                        value = color_sensor.get_value()
                        print(f"Value in {mode} mode: {value}")
                    sleep(DELAY_SEC)
            
            except KeyboardInterrupt:
                print("\nStopped by user.")
                reset_brick()
                break
            except Exception as e:
                print(f"Error: {e}")
                reset_brick()
                break
        else:
            print("Invalid mode. Please choose: component, ambient, red, rawred, id, or 'q' to quit.")
    
    reset_brick()
    print("Debug mode terminated.")
