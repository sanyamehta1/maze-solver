from point import Point
from cell import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.__win = win
        if seed is not None:
            seed = random.seed(seed)
        self.__cells = []

    def _create_cells(self):
        for i in range(self.num_rows):
            self.__cells.append([])
            for j in range(self.num_cols):
                p1 = Point(self.x1 + (j*self.cell_size_x), self.y1 + (i*self.cell_size_y))
                p2 = Point(p1.x + self.cell_size_x, p1.y + self.cell_size_y)
                self.__cells[i].append(Cell(p1, p2, self.__win)) # add self.__win back 

        if self.__win is not None:
            for i in range(self.num_rows):
                for j in range(self.num_cols):
                    self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        cell = self.__cells[i][j]
        cell.draw()

    def _animate(self):
        if self.__win is None:
            return 
        self.__win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit_cells(self):
        entrance_cell = self.__cells[0][0]
        exit_cell = self.__cells[self.num_rows - 1][self.num_cols - 1]
        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)
        exit_cell.has_bottom_wall = False
        self._draw_cell(self.num_rows - 1, self.num_cols - 1) 

    def _break_walls_r(self, i, j, counter):
        current_cell = self.__cells[i][j]
        current_cell.visited = True 

        while True:
            to_visit = []
            row_offsets = [1, 0, -1, 0]
            col_offsets = [0, 1, 0, -1]
            for d in range(4):
                new_row = i + row_offsets[d]
                new_col = j + col_offsets[d]
                cell_in_boundary = new_row >= 0 and new_row < self.num_rows and new_col >= 0 and new_col < self.num_cols
                if cell_in_boundary:
                    neighbor_cell = self.__cells[new_row][new_col]
                    if not neighbor_cell.visited:
                        to_visit.append((new_row, new_col))
            if len(to_visit) == 0:
                current_cell.draw()
                break
            else:
                index = random.randrange(len(to_visit))
                new_row = to_visit[index][0]
                new_col = to_visit[index][1]
                del to_visit[index]
                self._break_neighboring_walls(i, j, new_row, new_col)
                self._break_walls_r(new_row, new_col, counter)

    def _break_neighboring_walls(self, row1, col1, row2, col2):
        cell1 = self.__cells[row1][col1]
        cell2 = self.__cells[row2][col2]

        is_north = cell1.x1 == cell2.x1 and cell1.y1 == cell2.y2 
        is_east = cell1.y1 == cell2.y1 and cell1.x1 < cell2.x1
        is_south = cell1.x1 == cell2.x1 and cell1.y2 == cell2.y1
        is_west = cell1.y1 == cell2.y1 and cell1.x1 > cell2.x1 
 
        if is_north:
            cell1.has_top_wall = False
            cell2.has_bottom_wall = False
        if is_east:
            cell1.has_right_wall = False
            cell2.has_left_wall = False
        if is_south:
            cell1.has_bottom_wall = False
            cell2.has_top_wall = False
        if is_west:
            cell1.has_left_wall = False 
            cell2.has_right_wall = False 

    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                cell = self.__cells[i][j]
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self.__cells[i][j]
        current_cell.visited = True 
        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True
        
        row_offsets = [-1, 0, 1, 0]
        col_offsets = [0, -1, 0, 1]
        for d in range(4):
            new_row = i + row_offsets[d]
            new_col = j + col_offsets[d]
            cell_in_boundary = new_row >= 0 and new_row < self.num_rows and new_col >= 0 and new_col < self.num_cols
            if cell_in_boundary:
                neighbor_cell = self.__cells[new_row][new_col]
                if not neighbor_cell.visited:
                    is_wall = self._is_wall(current_cell, neighbor_cell)
                    if not is_wall:
                        current_cell.draw_move(neighbor_cell)
                        if self._solve_r(new_row, new_col):
                            return True 
                        current_cell.draw_move(neighbor_cell, undo=True)
        return False 

    def _is_wall(self, cell1, cell2):
        is_north = cell1.x1 == cell2.x1 and cell1.y1 == cell2.y2 
        is_east = cell1.y1 == cell2.y1 and cell1.x1 < cell2.x1
        is_south = cell1.x1 == cell2.x1 and cell1.y2 == cell2.y1
        is_west = cell1.y1 == cell2.y1 and cell1.x1 > cell2.x1 

        if is_north: 
            return self._is_wall_helper(cell1.has_top_wall, cell2.has_bottom_wall)
        if is_east:
           return self._is_wall_helper(cell1.has_right_wall, cell2.has_left_wall)
        if is_south:
            return self._is_wall_helper(cell1.has_bottom_wall, cell2.has_top_wall)
        if is_west:
            return self._is_wall_helper(cell1.has_left_wall, cell2.has_right_wall)
        
    def _is_wall_helper(self, wall1, wall2):
        if wall1 == False and wall2 == False:
            return False
        return True 

    def __str__(self):
        return f"Maze object: {self.num_rows} rows, {self.num_cols} columns, cell size: ({self.cell_size_x}, {self.cell_size_y})"
    
    def __repr__(self):
        return f"Maze({self.x1}, {self.y1}, {self.num_rows}, {self.num_cols}, {self.cell_size_x}, {self.cell_size_y})"



    

        

