from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__running = True
        self.__root.protocol('WM_DELETE_WINDOW', self.close)
        self.__canvas = Canvas(self.__root, bg='white', width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color='black'):
        line.draw(self.__canvas, fill_color)
    
class Point:
    def __init__(self, x, y):
        self.x = x 
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    
    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, 
            self.point1.y, 
            self.point2.x, 
            self.point2.y, 
            fill=fill_color, 
            width=2
        )
        canvas.pack()

class Cell:
    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            fill = 'black'
        else:
            fill = 'white'
        line = Line(Point(x1, y1), Point(x1, y2))
        self._win.draw_line(line, fill)
        if self.has_right_wall:
            fill = 'black'
        else:
            fill = 'white'
        line = Line(Point(x2, y1), Point(x2, y2))
        self._win.draw_line(line, fill)
        if self.has_bottom_wall:
            fill = 'black'
        else:
            fill = 'white'
        line = Line(Point(x1, y2), Point(x2, y2))
        self._win.draw_line(line, fill)
        if self.has_top_wall:
            fill = 'black'
        else:
            fill = 'white'
        line = Line(Point(x1, y1), Point(x2, y1))
        self._win.draw_line(line, fill)          

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return
        x_mid = (self._x1 + self._x2) / 2
        y_mid = (self._y1 + self._y2) / 2
        to_x_mid = (to_cell._x1 + to_cell._x2) / 2
        to_y_mid = (to_cell._y1 + to_cell._y2) / 2
        fill_color = "red"
        if undo:
            fill_color = "gray"
        if self._x1 > to_cell._x1:
            line = Line(Point(self._x1, y_mid), Point(x_mid, y_mid))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_y_mid), Point(to_cell._x2, to_y_mid))
            self._win.draw_line(line, fill_color)
        elif self._x1 < to_cell._x1:
            line = Line(Point(x_mid, y_mid), Point(self._x2, y_mid))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_cell._x1, to_y_mid), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)
        elif self._y1 > to_cell._y1:
            line = Line(Point(x_mid, y_mid), Point(x_mid, self._y1))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_cell._y2), Point(to_x_mid, to_y_mid))
            self._win.draw_line(line, fill_color)
        elif self._y1 < to_cell._y1:
            line = Line(Point(x_mid, y_mid), Point(x_mid, self._y2))
            self._win.draw_line(line, fill_color)
            line = Line(Point(to_x_mid, to_y_mid), Point(to_x_mid, to_cell._y1))
            self._win.draw_line(line, fill_color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        #each list index is a column, and contains a list of cells 
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        #draw each cell
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cells(i, j)
    
    def _draw_cells(self, i, j):
        if self._win is None:
            return
        #find x/y coordinates on window
        x1 = self._x1 + i * self._cell_size_x
        x2 = x1 + self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        y2 = y1 + self._cell_size_y
        #draw cell using x/y coordinates
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()
    
    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.02)
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cells(0, 0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cells(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []
            possible_direction_indexes = 0

            # check left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
                possible_direction_indexes += 1
            # check right
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
                possible_direction_indexes += 1
            # check up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
                possible_direction_indexes += 1
            # check down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))
                possible_direction_indexes += 1

            if possible_direction_indexes == 0:
                self._draw_cells(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(possible_direction_indexes)
            next_index = next_index_list[direction_index]

            # move right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # move left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # move down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # move up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        if self._solve_r(i=0, j=0):
            return True
        return False
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        
        current = self._cells[i][j]

        #left
        if (
            i > 0 
            and not current.has_left_wall 
            and not self._cells[i-1][j].visited
        ):
            current.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            else:
                current.draw_move(self._cells[i-1][j], True)
            self._solve_r(i-1, j)
        #right
        if (
            i < self._num_cols - 1 
            and not current.has_right_wall 
            and not self._cells[i+1][j].visited
        ):
            current.draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            else:
                current.draw_move(self._cells[i+1][j], True)
            self._solve_r(i+1, j)
        #up
        if (
            j > 0
            and not current.has_top_wall 
            and not self._cells[i][j+1].visited
        ):
            current.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            else:
                current.draw_move(self._cells[i][j+1], True)
            self._solve_r(i, j+1)    
        #down
        if (
            j < self._num_rows - 1 
            and not current.has_bottom_wall 
            and not self._cells[i][j-1].visited
        ):
            current.draw_move(self._cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            else:
                current.draw_move(self._cells[i][j-1], True)
            self._solve_r(i, j-1)
        
        return False

def main():
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)

    maze = Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win, 10)
    maze.solve()

    win.wait_for_close()

main()



