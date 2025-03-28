

NODE_PER_GRID = 2
GRID_HEIGHT = 2
GRID_LENGTH = 3


room = [[False]*(GRID_LENGTH*NODE_PER_GRID) for _ in range(GRID_HEIGHT*NODE_PER_GRID)]




def dfs(x, y):
    n, m = len(room), len(room[0])
    stack = [(x, y)]
    seen = set()
    while stack:
        x, y = stack.pop()
        if x < 0 or x >= n or y < 0 or y >= m or (x, y) in seen:
            continue
        seen.add((x, y))
        if not room[x][y]:
            room[x][y] = True
            return (x, y)
        stack.append((x-1, y))
        stack.append((x, y+1))
        stack.append((x, y-1))
        stack.append((x+1, y))
    return (-1, -1)

def navigate():
    x, y = 0, 3
    while (x, y) != (-1, -1):
        x, y = dfs(x, y)
        print(x, y)
    for line in room[::-1]:
        print(line)
    


    


def left():
    pass
def right():
    pass
def up():
    pass    
def down():
    pass

 
if __name__ == "__main__":
    navigate()