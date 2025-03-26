# config.py

# Sensor Ports
ULTRASONIC_SIDE_PORT = '1'  # X ultrasonic sensor 
ULTRASONIC_REAR_PORT = '2'  # Y ultrasonic sensor
COLOR_SENSOR_PORT = '3'  # Port for the color sensor
TOUCH_SENSOR_PORT = '4'  # Port for the touch sensor (emergency stop)

# Motor Ports
LEFT_MOTOR_PORT = 'B'  # Port for the left drive motor
RIGHT_MOTOR_PORT = 'C'  # Port for the right drive motor
SANDBAG_MOTOR_PORT = 'A'  # Port for the sandbag deployment motor

# Physical Constants
WHEEL_RADIUS = 2.8  # Wheel radius in cm
TRACK_WIDTH = 15.0  # Distance between wheels in cm
GRID_SIZE = 24.0  # Size of each grid cell in cm

# Sandbag Deployment
MAX_SANDBAGS = 5  # Maximum number of sandbags to deploy
SANDBAG_DEFAULT_DEG = 92  # Degrees to rotate for one sandbag deployment
SANDBAG_DEFAULT_DPS = 360  # Degrees per second for motor speed
SANDBAG_DEFAULT_POWER = 30

# Color Detection
COLOR_SENSOR_DELAY = 0.5  # Delay between color sensor readings (seconds)
COLOR_CSV_PATH = "src/data/color_log.csv"
COLOR_RED_CONFIRMATION_COUNT = 10
COLOR_COOLDOWN_DURATION = 10.0

# Siren
SIREN_DURATION = 0.5  # Duration of between siren note (seconds)
SIREN_NOTE_DURATION = 0.5  # Duration of each siren note (seconds)
SIREN_VOLUME = 80  # Volume of the siren (0-100)
