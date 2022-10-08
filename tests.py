import unittest
import intro

class TestCase(unittest.TestCase):
  
    def test1(self):
        expected = "Welcome to the game!"
        self.assertEqual(intro.game_start(), expected)
    
if __name__ == '__main__':
    unittest.main()
