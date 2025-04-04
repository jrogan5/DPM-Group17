
from config import *
from wheels import Wheels
from utils.brick import wait_ready_sensors
import time

class Navigation():
    
    def __init__(self, wheels=None, debug=False):
        self.room:list[bool] = [[False]*(GRID_LENGTH*NODE_PER_GRID) for _ in range(GRID_HEIGHT*NODE_PER_GRID)]
        self.wheels = wheels
        self.odometry = wheels.odometry
        self.debug = debug
        if debug:
            print("done initialising")
        

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

    def return_to_origin(self):
        "Return to the origin of the map, in absoulute coordinates"
        pass

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
    
if __name__ == "__main__":
    try:
        wait_ready_sensors(True)
        print("Navigation test")
        wheels = Wheels(debug=True)
        nav = Navigation(wheels=wheels, debug=True)
        nav.navigate_grid()
        while True:
            pass
    except KeyboardInterrupt:
        print(f"\nUser interrupt, exiting...")
    except Exception as e:
        print(f"Error: {e}")
