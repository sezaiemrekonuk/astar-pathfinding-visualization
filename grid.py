import pygame
import math

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = (255, 255, 255)  # White
        self.neighbors = []
        self.neighbor_costs = {}  # Store costs for each neighbor
        self.width = width
        self.total_rows = total_rows
        self.g_score = float('inf')
        self.h_score = float('inf')
        self.f_score = float('inf')

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == (255, 0, 0)  # Red

    def is_open(self):
        return self.color == (0, 255, 0)  # Green

    def is_barrier(self):
        return self.color == (0, 0, 0)  # Black

    def is_start(self):
        return self.color == (255, 165, 0)  # Orange

    def is_end(self):
        return self.color == (128, 0, 128)  # Purple

    def reset(self):
        self.color = (255, 255, 255)  # White
        self.g_score = float('inf')
        self.h_score = float('inf')
        self.f_score = float('inf')

    def make_closed(self):
        self.color = (255, 0, 0)  # Red

    def make_open(self):
        self.color = (0, 255, 0)  # Green

    def make_barrier(self):
        self.color = (0, 0, 0)  # Black

    def make_start(self):
        self.color = (255, 165, 0)  # Orange

    def make_end(self):
        self.color = (128, 0, 128)  # Purple

    def make_path(self):
        self.color = (64, 224, 208)  # Turquoise

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.width), 1)  # Black border
        
        # Only draw scores if they are not infinity and the node is not a barrier
        if not self.is_barrier() and self.f_score != float('inf'):
            font = pygame.font.SysFont('Arial', 8)
            
            # Draw G score (top left)
            g_text = font.render(f'G:{self.g_score:.1f}', True, (0, 0, 0))
            win.blit(g_text, (self.x + 2, self.y + 2))
            
            # Draw H score (top right)
            h_text = font.render(f'H:{self.h_score:.1f}', True, (0, 0, 0))
            win.blit(h_text, (self.x + self.width - h_text.get_width() - 2, self.y + 2))
            
            # Draw F score (center)
            f_text = font.render(f'F:{self.f_score:.1f}', True, (0, 0, 0))
            f_x = self.x + (self.width - f_text.get_width()) // 2
            f_y = self.y + (self.width - f_text.get_height()) // 2
            win.blit(f_text, (f_x, f_y))

    def update_neighbors(self, grid):
        self.neighbors = []
        self.neighbor_costs = {}
        
        # Check for neighbors in all eight directions
        # Cardinal directions (cost = 1)
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            neighbor = grid[self.row - 1][self.col]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = 1

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            neighbor = grid[self.row + 1][self.col]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = 1

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            neighbor = grid[self.row][self.col - 1]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = 1

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            neighbor = grid[self.row][self.col + 1]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = 1

        # Diagonal directions (cost = √2 ≈ 1.414)
        diagonal_cost = math.sqrt(2)
        
        # UP-LEFT
        if (self.row > 0 and self.col > 0 and 
            not grid[self.row - 1][self.col - 1].is_barrier() and
            not grid[self.row - 1][self.col].is_barrier() and  # Check if path is clear
            not grid[self.row][self.col - 1].is_barrier()):
            neighbor = grid[self.row - 1][self.col - 1]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = diagonal_cost

        # UP-RIGHT
        if (self.row > 0 and self.col < self.total_rows - 1 and 
            not grid[self.row - 1][self.col + 1].is_barrier() and
            not grid[self.row - 1][self.col].is_barrier() and  # Check if path is clear
            not grid[self.row][self.col + 1].is_barrier()):
            neighbor = grid[self.row - 1][self.col + 1]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = diagonal_cost

        # DOWN-LEFT
        if (self.row < self.total_rows - 1 and self.col > 0 and 
            not grid[self.row + 1][self.col - 1].is_barrier() and
            not grid[self.row + 1][self.col].is_barrier() and  # Check if path is clear
            not grid[self.row][self.col - 1].is_barrier()):
            neighbor = grid[self.row + 1][self.col - 1]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = diagonal_cost

        # DOWN-RIGHT
        if (self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and 
            not grid[self.row + 1][self.col + 1].is_barrier() and
            not grid[self.row + 1][self.col].is_barrier() and  # Check if path is clear
            not grid[self.row][self.col + 1].is_barrier()):
            neighbor = grid[self.row + 1][self.col + 1]
            self.neighbors.append(neighbor)
            self.neighbor_costs[neighbor] = diagonal_cost

class Grid:
    def __init__(self, rows, width):
        self.rows = rows
        self.width = width
        self.grid = []
        self.gap = width // rows
        self.make_grid()

    def make_grid(self):
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                node = Node(i, j, self.gap, self.rows)
                self.grid[i].append(node)

    def draw(self, win):
        for row in self.grid:
            for node in row:
                node.draw(win)

    def get_clicked_pos(self, pos):
        y, x = pos
        row = y // self.gap
        col = x // self.gap
        return row, col

    def reset(self):
        for row in self.grid:
            for node in row:
                node.reset() 