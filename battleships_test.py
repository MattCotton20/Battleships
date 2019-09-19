import unittest
from battleships import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        board = Board(4)
        board.place_ship(((0, 0), (0, 1)))
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
