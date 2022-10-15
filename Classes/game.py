from .player import Player


class Game:
    """
    Represents an instance of the game ScaryAttic.
    """
    def __init__(self, saveFile) -> None:
        self.running = True
        self.saveFile = saveFile
        self.currentSaveName = None
        self.rooms = {}
        self.items = {}
        self.player = Player()

    def isRunning(self):
        """
        Returns True if Game is still being played or False if user
        has exited the game.
        """
        return self.running

    def titleScreen(self):
        """
        Displays game title screen.
        """
        # TODO:: print title screen
        print("Welcome to the game! (placeholder)")
        print("Enter the command 'exit game' to stop playing.")

    def selectGameState(self):
        """
        Prompts the user to select a new game or load a saved game.
        """
        # TODO::
        # print message to input new game or load game
        # if new game, then load initial game state
        # else, then print names of available saveSates (not initial)
        #   take input for selected save and load corresponding saveState
        pass

    def saveGame(self):
        """
        Saves the current state of a Game to file.
        """
        if self.currentSaveName is None:
            # TODO:: Prompt user to enter new save name
            # Write saveState object to file with new save name
            # Set currentSaveName to new save name
            pass
        # TODO:: overwrite game state to saveState with name==currentSaveName
        # overwrite player inventory and location
        # overwrite room states

    def loadGame(self, loadName):
        """
        Loads a Game state from file.
        """
        # TODO:: Set state of game to state with loadName
        # Update user inventory and location states
        # Update room states
        self.currentSaveName = loadName

    def exitGame(self):
        """
        Confirms user input and terminates the current game instance.
        """
        print("Are you sure you want to exit the game? Any unsaved progress will be lost.")
        exitInput = input("Y / N: ").replace(" ", "").lower()
        while exitInput not in ["y", "yes", "n", "no"]:
            print("Your response was not valid. Are you sure you want to exit the game?")
            exitInput = input("Y / N: ").replace(" ", "").lower()
        if exitInput == "y" or exitInput == "yes":
            self.running = False
