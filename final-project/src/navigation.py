
from config import *
from wheels import Wheels
from odometry import Odometry
from utils.brick import reset_brick, wait_ready_sensors
import time

class Navigation():
    
    HARD_SWEEP_PATH: list[str] = [ # Used as worst-case scenrio for the demo. 
        ("N","fwd"),
        ("N","fwd"),
        ("N","fwd"),
        ("N","fwd"),
        ("N","fwd"),
        ("N","fwd"),
        # ("E","fwd"),("E","fwd"),("E","rev"),("E","rev"), 
        # ("W","fwd"), ("W","fwd"),("W","rev"),("W","rev"),
        ("N","fwd"),
        # ("E","fwd"),("E","fwd"),("E","rev"),("E","rev"), 
        # ("W","fwd"), ("W","fwd"),("W","rev"),("W","rev"),
        ("N","fwd"),
        # ("E","fwd"),("E","fwd"),("E","rev"),("E","rev"),
        # ("W","fwd"), ("W","fwd"),("W","rev"),("W","rev"),
        ("N","rev"),
        ("N","rev"),
        ("N","rev"),
        ("N","rev"),
        ("N","rev"),
        ("N","rev"),
        ("N","rev"),
        ("N","rev"),
    ]
    SWEEP_PATH: list[str] = [("x",(87.0, 85.4)),("y",(77.2, 97.5)),("x",(60.0, 104.4)),"face south","CCW adjust", "CW adjust"]

    
    def __init__(self, debug=False):
        self.room:list[bool] = [[False]*(GRID_LENGTH*NODE_PER_GRID) for _ in range(GRID_HEIGHT*NODE_PER_GRID)]
        self.debug = debug
        self.odometry = Odometry(debug=self.debug)
        self.wheels = Wheels(debug=False,odometry=self.odometry)
        self.use_odometry = False
        if debug:
            print("(Navigation) done initialising")

    def dfs(self, x, y):
        n, m = len(self.room), len(self.room[0])
        stack = [(x, y)] 
        seen = set()
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= m or y < 0 or y >= n or (x, y) in seen:
                continue
            seen.add((x, y))
            if not self.room[y][x]:
                self.room[y][x] = True
                return (x, y)
            stack.append((x-1, y))
            stack.append((x, y+1))
            stack.append((x, y-1))
            stack.append((x+1, y))
        return (-1, -1)

    def navigate_grid(self):
        # start with the grid position of the robot using odometry
        if self.debug:
            print("Inside navigate grid")
        time.sleep(5)
        xy_cm = self.odometry.get_xy(direction=self.wheels.direction)
        x, y = 3, 3
        if self.debug:
            print(f"Current position in cm {xy_cm}")
        #x, y = self._xy_to_grid(xy_cm)
        if self.debug:
            print(x, y)
        # then move onto the dfs search
        while (x, y) != (-1, -1):
            new_x, new_y = self.dfs(x, y)
            while new_x > x:
                self.wheels.move_direction("N", int(TILE_ANG // NODE_PER_GRID))
                x += 1
            while new_x < x:
                self.wheels.move_direction("S", int(TILE_ANG // NODE_PER_GRID))
                x -= 1
            while new_y > y:
                self.wheels.move_direction("W", int(TILE_ANG // NODE_PER_GRID))
                y += 1
            while new_y < y:
                self.wheels.move_direction("E", int(TILE_ANG // NODE_PER_GRID))
                y -= 1
            time.sleep(3)
            print(f"Current pos: {x, y}")
            for line in self.room:
                print(line)

    def start(self):
        if self.odometry is None:
            print("(Navigation) odometry not initialized")
            return
        if self.wheels is None:
            print("(Navigation) wheels not initialized")
        print("Wheels and Odometry started!")
        pos = self.odometry.get_xy(self.wheels.direction)
        grid_pos = nav._xy_to_grid(pos)
        print(f"(Navigation) START: Current position: {pos}. Current grid position: {grid_pos}.")
        # self.wheels.move_to_coord((pos[0]-20, pos[1]))
        
    def assume_entry_position(self):
        if self.use_odometry is False:
            self.wheels.hard_code_traversal_there()
            return True
        if START_XY is not None and self.odometry.at_position("N",START_XY):
            if self.debug:
                print("OK: Assuming entry position in 5 seconds:")
                # self.wheels.hard_code_traversal_there()
                for i in range (0,5):
                    print(f"...{5-i}")
            print("(Navigation) MOVING TO ENTRY POSITION")
            self.wheels.move_to_coord("y",TURN1_XY)
            self.wheels.move_to_coord("x",TURN2_XY)
            self.wheels.move_to_coord("y",ENTRY_XY)
            print("(Navigation) SUCCESS")
            return True
        else:
            print(f"WARNING: Robot is not at correct START position; adjust the position manually.")
            return False
            
    
    def assume_exit_position(self):
        self.wheels.wheels_init() # after sweep, reset the motor power
        if self.use_odometry is False:
            return True
        if EXIT_XY is not None:
            pos = self.odometry.get_xy(self.wheels.direction)
            print(f"OK: Assuming EXIT position: {EXIT_XY} from current position: {pos}.")
            self.wheels.move_to_coord("x",EXIT_XY) # set the x coordinate
            self.wheels.move_to_coord("y",EXIT_XY) # set the y coordinate
            self.wheels.face_direction("S") # set the direction
            if self.odometry.at_position("S", EXIT_XY):
                print("OK: Robot is at correct EXIT position.")
                return True
            else:
                print("WARNING: Robot is not at correct EXIT position; adjust the position manually.")
                return False
        else:
            print("WARNING: EXIT position not set. See config.py.")
            return False
        
    def return_to_start(self):
        self.wheels.wheels_return_init()
        if self.use_odometry is False:
            self.wheels.hard_code_traversal_back()
            return True
        if EXIT_XY is not None and self.odometry.at_position("S",EXIT_XY):
            print("OK: Returning to start.")
            #self.hard_code_traversal_back()
            self.wheels.move_to_coord("y",TURN3_XY)
            self.wheels.move_to_coord("x",TURN4_XY)
            self.wheels.move_to_coord("y",END_XY)
            return True
        else:
            print("WARNING: Robot is not at correct EXIT position; adjust the position manually.")
            return False
                

    def _xy_to_grid(self, xy:tuple[float, float])->tuple[int, int]:
        # converts the float x,y from the odometry to the integer grid coordinates row,col
        # xy[0] = absolute x coordinate, xy[1] = absolute y coordinate
        (x,y) = (xy[0]-KITCHEN_ORIGIN[0], xy[1]-KITCHEN_ORIGIN[1])
        row = int(x // GRID_LENGTH*NODE_PER_GRID)
        col = int(y // GRID_HEIGHT*NODE_PER_GRID)
        if row < 0 or row >= GRID_HEIGHT*NODE_PER_GRID or col < 0 or col >= GRID_LENGTH*NODE_PER_GRID:
            print(f"Invalid coordinates: {xy} (could not be converted to grid)")
            return (-1, -1)
        return (row, col)

    def hard_sweep_grid(self):
        if ENTRY_XY is not None and self.odometry.at_position("N",ENTRY_XY):
            if self.debug:
                print("OK: Starting hard sweep of the kitchen in 5 seconds...")
                for i in range (0,5):
                    print(f"...{5-i}")
            print("(Navigation) HARD SWEEPING KITCHEN")
            for direction in self.HARD_SWEEP_PATH:
                self.wheels.move_direction(direction, int(TILE_ANG // NODE_PER_GRID))
                self.wheels.wait_between_moves()
                time.sleep(2)
                print("Will sweep here")
            print("Sweep finished")
            return True
        else:
            print("WARNING: Robot is not at correct entry position.")
            return False
    
    
    
if __name__ == "__main__":
    try:
        nav = Navigation(debug=True)
        wait_ready_sensors(True)
        time.sleep(1)
        print("Navigation test")
        nav.start()
        # for i in range (0, 5):
        #     pos = nav.odometry.get_xy("N")
        #     grid_pos = nav._xy_to_grid(pos)
        #     print(f"{i}. Current position: {pos}. Current grid position: {grid_pos}")
        #     time.sleep(1)
        t_wait = 3
        print(f"Waiting {t_wait} seconds for the user to set up the robot at the start position")
        time.sleep(t_wait)
        if not nav.assume_entry_position():
            raise ValueError("Failiure on entry; see above.")
        if not nav.hard_sweep_grid_no_sweeper():
            raise ValueError("Failure on grid sweep; see above.")
        if not nav.assume_exit_position():
            raise ValueError("Failure on exit; see above.")
        if not nav.return_to_start():
            raise ValueError("Failiure on return; see above.")
            
        
        
    except KeyboardInterrupt:
        print(f"\nUser interrupt, exiting...")
        reset_brick()
    except Exception as e:
        print(f"Exception raised: {e}")
        reset_brick()

