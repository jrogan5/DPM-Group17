# config.py

# Sensor Ports
ULTRASONIC_SIDE_PORT = '1'  # X ultrasonic sensor 
ULTRASONIC_REAR_PORT = '2'  # Y ultrasonic sensor
COLOR_SENSOR_PORT = '4'  # Port for the color sensor
TOUCH_SENSOR_PORT = '3'  # Port for the touch sensor (emergency stop)

# Motor Ports
LEFT_MOTOR_PORT = 'D'  # Port for the left drive motor
RIGHT_MOTOR_PORT = 'C'  # Port for the right drive motor
SANDBAG_MOTOR_PORT = 'A'  # Port for the sandbag deployment motor
SWEEP_MOTOR_PORT = 'B'

# Physical Constants
WHEEL_RADIUS = 2.8  # Wheel radius in cm
TRACK_WIDTH = 15.0  # Distance between wheels in cm
GRID_SIZE = 24.0  # Size of each grid cell in cm

# Odometry Constants
DELAY_SEC = 1  # seconds of delay between measurements
TUNING_X= 3.4 # ((12.8-9.4)+(15.7-12.3))/2
TUNING_Y= 3.3 # ((14.8-11.6)+(16.5-13.2))/2
MAX_X=121.8 + TUNING_X #cm (see test report for derivation of tuning parameters)
MAX_Y=121.7 + TUNING_Y #cm
CEN_X=6.7  #cm from face of US_X, plus an additional tuning offset
CEN_Y=8.1  #cm from face of US_Y, plus an additional tuning offset

# Sandbag Deployment
MAX_SANDBAGS = 2  # Maximum number of sandbags to deploy
SANDBAG_DEFAULT_DEG = 92  # Degrees to rotate for one sandbag deployment
SANDBAG_DEFAULT_DPS = 360  # Degrees per second for motor speed
SANDBAG_DEFAULT_POWER = 30

# Color Detection
SENSOR_DELAY = 0.1  # Delay between sensor readings (seconds)
COLOR_CSV_PATH = "src/data/color_log.csv"
COLOR_RED_CONFIRMATION_COUNT = 5
COLOR_GREEN_CONFIRMATION_COUNT = 5
COLOR_COOLDOWN_DURATION = 10.0

# Siren
SIREN_DURATION = 0.5  # Duration of between siren note (seconds)
SIREN_NOTE_DURATION = 0.5  # Duration of each siren note (seconds)
SIREN_VOLUME = 80  # Volume of the siren (0-100)

# Wheels
BATTERY_NUM = 33
ANG_90 = 220
ANG_10 = int(250 // 9)
RW_ADJ = -4.5 # Right wheel adjustment, for power
TILE_ANG = 660
SWEEP_MOVE = 400
CCW_ADJ = -2
BAT_34_ADJ = 32 # Battery 34 adjustment
START_XY = (17.0, 13.0) # Starting coordinates for the robot
TURN1_XY = (15.8, 56.9) # entry
TURN2_XY = (80.9, 61.4) # entry
TURN3_XY = (85.9,72.1)  # exit
TURN4_XY = (55.7, 67.2) # exit
END_XY = (13.3, 25.2)
START_DIR = "N" # Starting direction for the robot
ENTRY_XY = (83.7, 80.7)
EXIT_XY = (87.7, 89.6) # Entrance coordinates for the robot
POS_THRESHOLD = 8 # Threshold for position accuracy in cm

# Navigation (in kitchen)
NODE_PER_GRID = 3
GRID_HEIGHT = 2
GRID_LENGTH = 3
KITCHEN_ORIGIN = (49.5,74.0) # bottom left corner of the kitchen

# Sweeper
SWEEP_MOTOR_LIMIT = 15 #MAXIMUM WITHOUT LOSING ACCURACY IS 17 -Eric (Tested plugged to wall)
SWEEP_RANGE = 140
SWEEP_POW_ADJ = -10 # Slows the motion while sweeping
# "Unlimited" or number
REFRESH_RATE = 0.1 # KEEP AT 0.1, LOWERING LOWERS ACCURACY -Eric (Tested Plugged to Wall)

