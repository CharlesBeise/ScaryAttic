from player import Player


class Game:
    """
    Represents an instance of the game ScaryAttic
    """
    def __init__(self) -> None:
        self.running = True
        self.currentSaveName = None
        self.rooms = {}
        self.items = {}
        self.player = Player()
        pass

    def saveGame(self):
        """Saves the current state of a Game to file"""
        pass

    def loadGame(self, loadName):
        """Loads a Game state from file"""
        pass

    def exitGame(self):
        """Terminates the current game instance"""
        self.running = False
