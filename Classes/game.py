import os
import time
from .player import Player
from .room import Room


class Game:
    """
    Represents an instance of the game ScaryAttic.
    """
    def __init__(self, saveFile) -> None:
        self.running = True
        self.saveFile = saveFile
        self.currentSaveName = None
        self.rooms = []
        self.items = []
        self.player = Player()

        # Build instances of all the rooms
        self.buildRooms()
        # TODO: Rooms will need to be connected after all Rooms are created

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

    def newGameIntro(self):
        """
        Displays introduction at the start of a new game.
        """
        part1 = """It's your first night in the new house. An old 2-story Victorian-style home nestled
             just outside the city. Most of your belongings are still scattered in boxes around the house.
             For tonight, it's just you and the mattress on the floor."""
        part2 = """Somehow you're both exhausted from the move and unable to sleep. This is your first
             time seeing the house at night. Built a hundred years ago, the house is full of old wood,
             metal, and unfamiliar sounds. Rain starts to patter against the bedroom window."""
        part3 = """Just as you start to drift off to sleep, you hear a THUMP from downstairs. It was
             loud, and you can't push it out of your mind. With a sigh, you get up to have a look and
             turn on the light. Suddenly, a flash fills the room and you hear the rumbling clap of thunder.
             The power in the house cuts out. Downstairs, you hear it again… THUMP."""
        print(part1)
        time.sleep(10)
        print(part2)
        time.sleep(10)
        print(part3)
        time.sleep(10)

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

    def buildRooms(self):
        """
        Builds room instances automatically from files
        """
        # Iterate through all Room JSON Files and build the instances
        room_dir = "Rooms"
        for filename in os.listdir(room_dir):
            file = os.path.join(room_dir, filename)
            # If it's a valid file, create the Room
            if os.path.isfile(file):
                self.rooms.append(Room(file))
