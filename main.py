from graphics import Window
from point import Point
from line import Line
from cell import Cell
from maze import Maze

def main():
    win = Window(800, 600)

    """
    cell1 = Cell(Point(40, 60), Point(60, 80), win, has_top_wall=False)
    cell2 = Cell(Point(80, 60), Point(60, 80), win, has_bottom_wall=False)
    print(cell1)
    print(cell2)
    cell1.draw()
    cell2.draw()
    cell1.draw_move(cell2, undo=True)
    # line.draw(Point(50, 50), Point(50, 40))
    """

    m1 = Maze(0, 0, 5, 5, 100, 100, win)
    m1._create_cells()
    m1._animate()
    m1._break_entrance_and_exit_cells()
    m1._break_walls_r(0, 0, 0)
    m1._reset_cells_visited()
    print(m1.solve())

    win.wait_for_close()

main()