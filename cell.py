from point import Point
from line import Line

class Cell:
    def __init__(self, p1, p2, win=None, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.x1 = p1.x
        self.y1 = p1.y
        self.x2 = p2.x
        self.y2 = p2.y
        self.__win = win
        self.visited = False
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall

    def get_center_coordinates(self):
        x = (self.x1 + self.x2)//2
        y = (self.y1 + self.y2)//2
        return Point(x, y)

    def draw(self):
        # for this system, y1 is always smaller than y2 (so it increases downward)
        if self.__win is not None: 
            left_line = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            right_line = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            top_line = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            bottom_line = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))

            if self.has_left_wall:
                self.__win.draw_line(left_line)
            else:
              self.__win.draw_line(left_line, "white")

            if self.has_right_wall:
                self.__win.draw_line(right_line)
            else: 
              self.__win.draw_line(right_line, "white")

            if self.has_top_wall:
                self.__win.draw_line(top_line)
            else: 
                self.__win.draw_line(top_line, "white")

            if self.has_bottom_wall:
                self.__win.draw_line(bottom_line)
            else:
              self.__win.draw_line(bottom_line, "white")
        """
        else:
            print("Cannot draw: no window provided")
        """

    def draw_move(self, to_cell, undo=False):
        # draw a line from the center of one cell to another
        if undo:
            fill_color = "gray"
        else: 
            fill_color = "red"
            
        p1 = self.get_center_coordinates()
        p2 = to_cell.get_center_coordinates()
        line = Line(p1, p2)
        self.__win.draw_line(line, fill_color)

    def __str__(self):
         p1 = Point(self.x1, self.y1)
         p2 = Point(self.x2, self.y2)

         return f"Cell object: p1 = {p1}, p2 = {p2}, bottom wall = {self.has_bottom_wall}, top wall = {self.has_top_wall}, left wall = {self.has_left_wall}, right wall = {self.has_right_wall}, visited = {self.visited}"


