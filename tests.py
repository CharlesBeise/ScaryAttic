import unittest
import main
import sys
from io import StringIO
from Classes.game import Game
from Classes.player import Player


class TestCase(unittest.TestCase):

    def test1(self):
        # Redirect stdout to test output to console
        testOutput = StringIO()
        sys.stdout = testOutput
        testFile = "testSaveStates.json"
        testGame = Game(testFile)
        testGame.titleScreen()
        expected = "Welcome to the game! (placeholder)\nEnter the command 'exit game' to stop playing.\n"
        self.assertEqual(testOutput.getvalue(), expected)


if __name__ == '__main__':
    unittest.main()
