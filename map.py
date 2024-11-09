import random
import numpy as np

class Cell:
    def __init__(self):
        self.parent_x = 0  # Parent cell's row index
        self.parent_y = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination
        
class Map:
    def __init__(self, width, height, src_point=(0,0), des_point=(0,0)):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        if src_point != des_point:
            self.src_point = src_point
            self.des_point = des_point
        else: self.CreateSrcDes()
        self.grid[self.src_point[1]][self.src_point[0]] = 2
        self.grid[self.des_point[1]][self.des_point[0]] = 3

    def CreateSrcDes(self):
        self.src_point = (random.randint(0, self.width-1), 0)
        self.des_point = (random.randint(0, self.width-1), self.height-1)
    def CreateWall(self, wall_rate=0.3):
        for i in range(self.width):
            for j in range(self.height):
                if (i, j) != self.src_point and (i, j) != self.des_point:
                    self.grid[j][i] = int(random.random()<=wall_rate)
    def IsValid(self, x, y):
        return (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height)
    def IsBlock(self, x, y):
        return self.grid[y][x] == 1
    def IsDestination(self, x, y):
        return self.grid[y][x] == 3
    def CalculateH(self, x, y):
        # return ((x - self.des_point[0]) ** 2 + (y - self.des_point[1]) ** 2) ** 0.5
        return abs(x - self.des_point[0]) + abs(y - self.des_point[1])
    