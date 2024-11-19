import random
import numpy as np

# Class map để tạo và quản lí bản đồ cho bài toán tìm đường
class Map:
    def __init__(self, width, height, src_point=(0,0), des_point=(0,0)):
        self.width = width # Chiều dài bản đồ
        self.height = height # Chiều rộng bản đồ
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
    
    def load_from_file(self, filename):
        """Đọc bản đồ từ file txt
        Format file:
        - Dòng đầu tiên chứa 2 số: chiều rộng (width) và chiều cao (height)
        - Các dòng tiếp theo là ma trận bản đồ với:
            0: lối đi
            1: tường
            2: điểm bắt đầu
            3: điểm đích
        """
        try:
            with open(filename, 'r') as f:
                # Đọc kích thước bản đồ
                self.width, self.height = map(int, f.readline().split())

                # Khởi tạo grid rỗng
                self.grid = []

                # Đọc từng dòng của bản đồ
                for _ in range(self.height):
                    row = list(map(int, f.readline().split()))
                    if len(row) != self.width:
                        raise ValueError("Chiều rộng của map không khớp")
                    self.grid.append(row)

                # Tìm điểm bắt đầu và điểm đích
                self.src_point = None
                self.des_point = None

                for y in range(self.height):
                    for x in range(self.width):
                        if self.grid[y][x] == 2:
                            if self.src_point is not None:
                                raise ValueError(
                                    "Có nhiều hơn một điểm bắt đầu")
                            self.src_point = (x, y)
                        elif self.grid[y][x] == 3:
                            if self.des_point is not None:
                                raise ValueError("Có nhiều hơn một điểm đích")
                            self.des_point = (x, y)

                if self.src_point is None:
                    raise ValueError("Không tìm thấy điểm bắt đầu")
                if self.des_point is None:
                    raise ValueError("Không tìm thấy điểm đích")

                return True

        except FileNotFoundError:
            print(f"Không tìm thấy file {filename}")
            return False
        except Exception as e:
            print(f"Lỗi khi đọc file: {str(e)}")
            return False

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
    