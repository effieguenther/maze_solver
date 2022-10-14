from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("window")
        self.__canvas = Canvas(self.__root, bg='white', width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol('WM_DELETE_WINDOW', self.close)

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

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)
    
    def draw_cell(self, cell, fill_color):
        cell.draw(self.__canvas, fill_color)

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
    def __init__(self, point1, point2):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = point1.x
        self.__x2 = point2.x
        self.__y1 = point1.y
        self.__y2 = point2.y

    def draw(self, canvas, fill_color):
        if self.has_left_wall:
            canvas.create_line(
            self.__x1, 
            self.__y2, 
            self.__x1, 
            self.__y1, 
            fill=fill_color, 
            width=2
            )
            canvas.pack()
        if self.has_right_wall:
            canvas.create_line(
            self.__x2, 
            self.__y2, 
            self.__x2, 
            self.__y1, 
            fill=fill_color, 
            width=2
            )
            canvas.pack()
        if self.has_bottom_wall:
            canvas.create_line(
            self.__x1, 
            self.__y2, 
            self.__x2, 
            self.__y2, 
            fill=fill_color, 
            width=2
            )
            canvas.pack()
        if self.has_top_wall:
            canvas.create_line(
            self.__x1, 
            self.__y1, 
            self.__x2, 
            self.__y1, 
            fill=fill_color, 
            width=2
            )
            canvas.pack()            


def main():
    win = Window(800, 600)
    win.wait_for_close()

main()



