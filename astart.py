import heapq
class AStart:
    def __init__(self, map):
        self.map = map
        self.cellinfo = map.cellinfo

    def Search(self):
        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.map.width)] for _ in range(self.map.height)]

        # Initialize the start cell details
        x = int(self.map.src_point[0])
        y = int(self.map.src_point[1])
        self.cellinfo[y][x].f = 0
        self.cellinfo[y][x].g = 0
        self.cellinfo[y][x].h = 0
        self.cellinfo[y][x].parent_x = x
        self.cellinfo[y][x].parent_y = y

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, x, y))

        # Initialize the flag for whether destination is found
        found_dest = False

        # Main loop of A* search algorithm
        while len(open_list) > 0:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)

            # Mark the cell as visited
            x = p[1]
            y = p[2]
            closed_list[y][x] = True

            # For each direction, check the successors
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dir in directions:
                new_x = x + dir[0]
                new_y = y + dir[1]

                # If the successor is valid, unblocked, and not visited
                if self.map.IsValid(new_x, new_y) and not self.map.IsBlock(new_x, new_y) and not closed_list[new_x][new_y]:
                    # If the successor is the destination
                    if self.map.IsDestination(new_x, new_y):
                        # Set the parent of the destination cell
                        self.cellinfo[new_y][new_x].parent_x = x
                        self.cellinfo[new_y][new_x].parent_y = y
                        print("The destination cell is found")
                        found_dest = True
                        return
                    else:
                        # Calculate the new f, g, and h values
                        g_new = self.cellinfo[y][x].g + 1.0
                        h_new = self.map.CalculateH(new_x, new_y, 'euclide')
                        #h_new = self.map.CalculateH(new_x, new_y, 'manhattan')
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if self.cellinfo[new_y][new_x].f == float('inf') or self.cellinfo[new_y][new_x].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_x, new_y))
                            # Update the cell details
                            self.cellinfo[new_y][new_x].f = f_new
                            self.cellinfo[new_y][new_x].g = g_new
                            self.cellinfo[new_y][new_x].h = h_new
                            self.cellinfo[new_y][new_x].parent_x = x
                            self.cellinfo[new_y][new_x].parent_y = y

        # If the destination is not found after visiting all cells
        if not found_dest:
            print("Failed to find the destination cell")
            return
    
    def PrintPath(self):
        print("The Path is ")
        path = []
        x = self.map.des_point[0]
        y = self.map.des_point[1]

        # Trace the path from destination to source using parent cells
        while not (self.cellinfo[y][x].parent_x == x and self.cellinfo[y][x].parent_y == y):
            path.append((x, y))
            temp_x = self.cellinfo[y][x].parent_x
            temp_y = self.cellinfo[y][x].parent_y
            x = temp_x
            y = temp_y

        # Add the source cell to the path
        path.append((x, y))
        # Reverse the path to get the path from source to destination
        path.reverse()

        # Print the path
        for i in path:
            print("->", i, end=" ")
        print()

    def UpdateGrid(self):
        x = self.map.des_point[0]
        y = self.map.des_point[1]

        # Trace the path from destination to source using parent cells
        while not (self.cellinfo[y][x].parent_x == x and self.cellinfo[y][x].parent_y == y):
            temp_x = self.cellinfo[y][x].parent_x
            temp_y = self.cellinfo[y][x].parent_y
            x = temp_x
            y = temp_y
            self.map.grid[y][x] = 4
        self.map.grid[y][x] = 2
        