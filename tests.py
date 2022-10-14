import unittest
import main


class TestCase(unittest.TestCase):

    def test1(self):
        expected = "Welcome to the game!"
        self.assertEqual(main.game_start(), expected)


if __name__ == '__main__':
    unittest.main()
