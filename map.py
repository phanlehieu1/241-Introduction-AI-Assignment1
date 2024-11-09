import random
import numpy as np

# Class cell để lưu lại các thông số của từng ô
class Cell:
    def __init__(self):
        self.parent_x = 0  # Parent cell's row index
        self.parent_y = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination

# Class map để tạo và quản lí bản đồ cho bài toán tìm đường
class Map:
    def __init__(self, width, height, src_point=(0,0), des_point=(0,0)):
        self.width = width # Chiều dài bản đồ
        self.height = height # Chiều rộng bản đồ
        self.cellinfo = [[Cell() for _ in range(width)] for _ in range(height)] # Tạo ma trận object cell lưu thông tin từng ô
        self.grid = np.zeros((height, width), dtype=int) # Tạo ma trận bản đồ 
        # 0: Lối đi
        # 1: tường vật cản
        # 2: điểm bắt đầu
        # 3: điểm kết thúc

        # Nếu không set điểm đầu/cuối thì sẽ tạo ngẫu nhiên
        if src_point != des_point: 
            self.src_point = src_point
            self.des_point = des_point
        else: self.CreateSrcDes()
        self.grid[self.src_point[1]][self.src_point[0]] = 2
        self.grid[self.des_point[1]][self.des_point[0]] = 3

    def CreateSrcDes(self):
        self.src_point = (random.randint(0, self.width-1), 0)
        self.des_point = (random.randint(0, self.width-1), self.height-1)

    # Tạo ngẫu nhiên tường/vật cản, mặc đinh khoảng 30% vật cản
    def CreateWall(self, wall_rate=0.3):
        for i in range(self.width):
            for j in range(self.height):
                if (i, j) != self.src_point and (i, j) != self.des_point:
                    self.grid[j][i] = int(random.random()<=wall_rate)
    
    # Kiểm tra vị trí x,y có tồn tại trên bản đồ
    def IsValid(self, x, y):
        return (x >= 0) and (x < self.width) and (y >= 0) and (y < self.height)
    
    # Kiểm tra vị trí x,y có bị chặn
    def IsBlock(self, x, y):
        return self.grid[y][x] == 1
    
    # Kiểm tra vị trí x,y có phải đích đến
    def IsDestination(self, x, y):
        return self.grid[y][x] == 3
    
    # Tính tianf hàm lượng giác h
    def CalculateH(self, x, y, algorithm):
        if algorithm == 'euclide':
            # Khoảng cách Euclid tính theo đường chéo từ điểm hiện tại đến đích dành cho di chuyển 8 hướng
            return ((x - self.des_point[0]) ** 2 + (y - self.des_point[1]) ** 2) ** 0.5 
        elif algorithm == 'manhattan':
            # Khoảng cách Manhattan tính theo đường thảng từ điểm hiện tại đến đích dành cho di chuyển 4 hướng
            return abs(x - self.des_point[0]) + abs(y - self.des_point[1])
    