# config.py

# Sensor Ports
COLOR_SENSOR_PORT = '1'  # Port for the color sensor
ULTRASONIC_REAR_PORT = '2'  # South-facing ultrasonic sensor
ULTRASONIC_SIDE_PORT = '3'  # East-facing ultrasonic sensor
TOUCH_SENSOR_PORT = '4'  # Port for the touch sensor (emergency stop)

# Motor Ports
LEFT_MOTOR_PORT = 'A'  # Port for the left drive motor
RIGHT_MOTOR_PORT = 'B'  # Port for the right drive motor
SANDBAG_MOTOR_PORT = 'C'  # Port for the sandbag deployment motor

# Physical Constants
WHEEL_RADIUS = 2.8  # Wheel radius in cm
TRACK_WIDTH = 15.0  # Distance between wheels in cm
GRID_SIZE = 24.0  # Size of each grid cell in cm