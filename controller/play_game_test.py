import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..')))

import unittest
from controller import play_game


class TestRollDice(unittest.TestCase):
    def test_roll_dice(self):
        # Act
        roll = play_game.roll_dice()

        # Assert
        self.assertGreaterEqual(roll, 1)
        self.assertLessEqual(roll, 6)


if __name__ == '__main__':
    unittest.main()
