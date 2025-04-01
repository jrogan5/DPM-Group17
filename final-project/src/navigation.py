

NODE_PER_GRID = 2
GRID_HEIGHT = 2
GRID_LENGTH = 3
from Wheels import Wheels

class Navigation():
    
    def __init__(self, wheels:Wheels=None, debug=False):
        self.room:list[bool] = [[False]*(GRID_LENGTH*NODE_PER_GRID) for _ in range(GRID_HEIGHT*NODE_PER_GRID)]
        self.wheels: Wheels
        if not Wheels:
            self.Wheels = Wheels()
        else:
            self.Wheels = wheels

    def dfs(self, x, y):
        n, m = len(self.room), len(self.room[0])
        stack = [(x, y)]
        seen = set()
        while stack:
            x, y = stack.pop()
            if x < 0 or x >= n or y < 0 or y >= m or (x, y) in seen:
                continue
            seen.add((x, y))
            if not self.room[x][y]:
                self.room[x][y] = True
                return (x, y)
            stack.append((x-1, y))
            stack.append((x, y+1))
            stack.append((x, y-1))
            stack.append((x+1, y))
        return (-1, -1)

    def navigate(self):
        x, y = 0, 3
        while (x, y) != (-1, -1):
            new_x, new_y = self.dfs(x, y)
            while new_x > x:
                self.wheels.move_direction("N")
                x += 1
            while new_x < x:
                self.wheels.move_direction("S")
                x -= 1
            while new_y > y:
                self.wheels.move_direction("E")
                y += 1
            while new_y < y:
                self.wheels.move_direction("W")
                y -= 1
            print(x, y)
        for line in self.room[::-1]:
            print(line)
        




 
if __name__ == "__main__":
    navigate()