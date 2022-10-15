import unittest
from main import Maze

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

if __name__ == "__main__":
    unittest.main()
