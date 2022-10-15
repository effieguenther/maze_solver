import unittest
from main import Maze
import random

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

        m2 = Maze(5, 5, 100, 500, 1, 1)
        self.assertEqual(len(m2._cells), 500)
        self.assertEqual(len(m2._cells[0]), 100)

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(m1._cells[5][5].visited)
        self.assertFalse(m1._cells[0][9].visited)

if __name__ == "__main__":
    unittest.main()
