# Firefighter Rescue Robot

## Project Overview

The Firefighter Rescue Robot is an autonomous robotic system designed for the ECSE 211 project at McGill University. Built using LEGO components and the BrickPi platform, this robot navigates a 1.2m x 1.2m simulated building environment, detects and extinguishes fires (represented by red stickers) by deploying foam cubes, avoids obstacles (green stickers), and returns to its base within 3 minutes. The project integrates hardware and software subsystems to achieve a robust, user-friendly design aligned with functional and non-functional requirements.

**Authors**: D. Vo, J. Rogan, L. Cai, E. Deng, B. Morava.
**Date**: March 23, 2025  
**Revision**: Initial draft based on brainstorming sessions and system design (V1.1 - V1.3)

---

## System Architecture

The robot is divided into two primary subsystems, each with four sub-subsystems, as depicted in *Figure 1: System Hierarchical Diagram*. Interactions between components are shown with blue arrows in the diagram.

### Hardware Subsystem
Responsible for physical construction, mobility, sensing, and peripheral interactions.

- **Structures**  
  - *Sandbag Deployment Mechanism*: A chute/funnel structure stores two foam cubes (2.54 cm³), with a minimum width of 2.60 cm and length of 5.20 cm. Inclined to use gravity for deployment.  
  - *Rear Drive Structure*: Supports two EV3 heavy motors and a ball bearing for stability.  
  - *Chassis*: Accommodates a 3 cm x 5 cm battery.  

- **Feature Detection**  
  - Two ultrasonic sensors (front and right) detect map edges for navigation.  
  - A color sensor on an extended, downward-angled arm detects red (fires) and green (obstacles) stickers within 1-5 cm.  

- **Mobility**  
  - Two EV3 heavy motors with rubber wheels enable a differential drive mechanism for straight-line movement and on-the-spot turns.  

- **Peripherals**  
  - *Emergency Stop (E-Stop)*: Touch sensor with secure mounting, connected via Micro-USB and AUX.  
  - *Speaker*: Mounted to play a fire truck siren.  

### Software Subsystem
Handles navigation, movement control, obstacle avoidance, fire extinguishing, and peripheral interactions.

- **Navigation and Obstacle Avoidance**  
  - Reads sensor data to position the robot in 2D space (X, Y coordinates) and avoid obstacles.  
  - Updates orientation (90° increments) for accurate mapping.  

- **Movement Control**  
  - Manages motor power, speed, and direction based on sensor inputs for translation and rotation.  

- **Fire Extinguishing**  
  - Detects fires via the color sensor and triggers sandbag deployment (one cube per fire).  

- **Peripherals**  
  - *E-Stop*: Halts all processes when triggered.  
  - *Speaker*: Plays siren until the fire room is reached.  

> [!Important]
>  The software relies on hardware sensor data and motor control, requiring tight integration for mission success.

---

## System Interactions

### Hardware ⇌ Software
- Software reads and analyzes sensor data from hardware (ultrasonic, color, touch).  
- Software sets motor parameters (power, speed, direction) to achieve navigation goals.  
- Peripherals (speaker, e-stop) require synchronized hardware-software functionality.

### Sub-Subsystem Interactions
- **Hardware**:  
  - *Structures ⇌ Feature Detection*: Sensor mounts ensure accurate positioning.  
  - *Structures ⇌ Mobility*: Rear drive supports motors and wheels.  
- **Software**:  
  - *Navigation ⇌ Movement Control*: Seamlessly detects obstacles/walls and adjusts movement.  
  - *Navigation ⇌ Fire Extinguishing*: Shares sensor data to trigger sandbag deployment.

---

## Design Specifications

### System-Level Specifications
- **Navigation**: Tracks position on a 1.2m x 1.2m grid using outer walls, follows a path to room #2, and returns to base (0,0).  
- **Obstacle Avoidance**: Detects and avoids green stickers without contact.  
- **Fire Extinguishing**: Detects and extinguishes two red stickers with foam cubes.  
- **Mobility**: Moves in straight lines with precise differential drive control.  
- **Peripheral Integration**: Incorporates touch sensor (e-stop) and speaker (siren).

### Hardware Specifications (*Figure 2: Hardware Subsystem Hierarchical Diagram*)
- **Sandbag Mechanism**: Chute with 2.60 cm width, 5.20 cm length, gravity-assisted.  
- **Sensors**: Two ultrasonic (front, right), one color (front, angled), touch (e-stop), speaker.  
- **Motors**: Two EV3 heavy motors with rubber wheels, ball bearing for stability.  

### Software Specifications (*Figure 3: Software Subsystem Hierarchical Diagram*)
- **Color Detection**: Detects red/green stickers within 1-5 cm using pre-defined color mappings.  
- **Sandbag Deployment**: Three states (hold, release #1, release #2) ensure one cube per fire.  
- **Movement**: Guided by ultrasonic data for translation and 90° turns.  

> [!WARNING]
> The robot must not exceed 20 cm width or 25 cm length to navigate the 22 cm door and 72x48 cm fire room.

---

## Requirements

### Functional Requirements
- Detect red stickers (fires) and deploy foam cubes.  
- Navigate 1.2m x 1.2m environment, avoiding green stickers and walls.  
- Start at (0,0), return within 3 minutes.  
- Include e-stop and siren features.

### Non-Functional Requirements
- **Performance**: Complete mission in 3 minutes, reliable fire detection/extinguishing.  
- **Reliability**: Avoid collisions, ensure e-stop functionality.  
- **Usability**: Easy to operate and reset, audible siren.

### Constraints
- Use LEGO + BrickPi materials only (no 3D printing).  
- Max width: 20 cm, max length: 25 cm.  
- Navigation to/from entrance: ≤45 seconds, leaving 90 seconds for fire tasks.


> [!NOTE]
> Sticker positions are unknown beforehand, requiring dynamic detection.

---

## Software Design

### Folder Structure

```firefighter_robot/
├── config.py          # Hardware ports and constants
├── navigation.py      # Movement and positioning logic
├── sensors.py         # Sensor data processing
├── fire_extinguisher.py # Sandbag deployment control
├── sound.py           # Siren playback
├── main.py            # Mission orchestration
└── data/              # Logs (e.g., color_log.csv)

```

### Key Components
- **config.py**: Defines ports (e.g., `COLOR_SENSOR_PORT = '1'`) and constants (e.g., `GRID_SIZE = 25.0`).  
- **navigation.py**: Controls differential drive motors for movement and turns.  
- **sensors.py**: Manages ultrasonic (distance) and color (RGB) sensors.  
- **fire_extinguisher.py**: `SandbagDispenser` class rotates a motor to deploy cubes.  
- **sound.py**: Plays/stops the siren using pygame.  
- **main.py**: Executes the mission: navigate to room #2, extinguish fires, return to base.

> [!TIP]
> Run `python main.py` to start the mission. Use individual files’ test blocks (e.g., `python fire_extinguisher.py`) for debugging.

### Efficiency Features
- **CSV Logging**: File opened once in `main.py` to reduce latency, with a flush option at startup.  
- **Color Detection**: `ColorDetector` class logs elapsed time and iterations to `data/color_log.csv`.

---

## Hardware Design

### Sandbag Deployment
- **Final Design**: Based on V1.3 (rotational gate), uses one medium motor to release cubes from an inclined chute.  
- **Pros**: Simple, single-motor solution.  
- **Cons**: Requires precise motor control to avoid jamming.

### Mobility
- Two EV3 motors with wheels, supported by a rear ball bearing for stability.

### Sensors
- **Ultrasonic**: Front and right for X, Y positioning.  
- **Color**: Front-mounted, angled downward for sticker detection.

> [!CAUTION]
> Ensure sensor mounts are secure; misalignment can lead to navigation errors.

---

## Brainstorming Insights

### Hardware Iterations
- **V1.1**: Dual-motor sandbag mechanism (too complex).  
- **V1.2**: Rotating platform (risk of jamming).  
- **V1.3**: Single-motor gate with chute (selected for simplicity).  

### Software Considerations
- **Pros**: Modular design, concurrent siren/e-stop threads.  
- **Cons**: Threading overhead manageable with careful synchronization.

---

## Setup and Usage

1. **Hardware Assembly**  
   - Build per *Figure 2* specifications using LEGO and BrickPi components.  
   - Connect sensors and motors to ports defined in `config.py`.

2. **Software Installation**  
   - Clone the repository: `git clone <repo-url>`.  
   - Install dependencies: `pip install brickpi3 pygame`.

3. **Running the Robot**  
   - Execute `python main.py`.  
   - At startup, choose to flush `color_log.csv` (y/n).  
   - Monitor console output and CSV logs in `data/`.

> [!TIP]
> Test sensors individually before full integration to isolate issues.

---

## Team and Project Management

- **Team**: 5 members, 9 hours/week each.  
- **Meetings**: Fridays 2-4 PM, emergency Discord calls as needed.  
- **Tools**: Timesheet for availability, Availabilities doc updated weekly.

> [!WARNING]
> Adhere to the 3-minute mission time; exceeding it risks point deductions.

---

## Scoring Features
| Feature                          | Points |
|----------------------------------|--------|
| Accesses room #2                 | +1     |
| Detects a fire                   | +1     |
| Extinguishes a fire              | +1     |
| Detects/extinguishes fire #2     | +1     |
| Completes mission in 3 minutes   | +1     |
| Returns to base                  | +1     |
| E-stop functions                 | +1     |
| Plays siren                      | +1     |
| Collides with object/wall        | -1     |
| Accesses wrong room              | -1     |
| Requires manual aid              | -1     |

---

## Figures
- *Figure 1*: System Hierarchical Diagram (see design doc).  
- *Figure 2*: Hardware Subsystem Diagram.  
- *Figure 3*: Software Subsystem Diagram.

---

## License
This project is for educational purposes under the ECSE 211 course at McGill University. All rights reserved by the team.

