import unittest
from point import Point
from cell import Cell 
from maze import Maze

class Tests(unittest.TestCase):
    num_rows = 12
    num_cols = 10

    def test_maze_create_cells(self):
        m1 = Maze(0, 0, self.num_rows, self.num_cols, 10, 10)
        m1._create_cells()
        self.assertEqual(len(m1._Maze__cells), self.num_rows)
        self.assertEqual(len(m1._Maze__cells[0]), self.num_cols)

    def test_break_entrance_and_exit_cells(self):
        m1 = Maze(0, 0, self.num_rows, self.num_cols, 10, 10)
        m1._create_cells()
        m1._break_entrance_and_exit_cells()
        self.assertEqual(m1._Maze__cells[0][0].has_top_wall, False)
        self.assertEqual(m1._Maze__cells[self.num_rows - 1][self.num_cols - 1].has_bottom_wall, False)

    def test_reset_cells_visited(self):
         m1 = Maze(0, 0, self.num_rows, self.num_cols, 10, 10)
         m1._create_cells()
         m1._break_walls_r(0, 0)
         m1._reset_cells_visited()
         for row in range(len(m1._Maze__cells)):
             for col in range(len(m1._Maze__cells[0])):
                 self.assertFalse(m1._Maze__cells[row][col].visited)
    
    def test_is_wall(self):
        m1 = Maze(0, 0, 1, 2, 10, 10)
        m1._create_cells()
        cell1 = m1._Maze__cells[0][0]
        cell2 = m1._Maze__cells[0][1]
        cell1.has_right_wall = False 
        self.assertFalse(m1._is_wall(cell1, cell2))
    
    
if __name__ == "__main__":
    unittest.main()
