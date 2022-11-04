import json
import os
import time
from .player import Player
from .room import Room
from .items import Item


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
        self.buildItems()
        self.setStartRoom()

    def getRooms(self):
        """
        Returns the list of Room objects in the game
        """
        return self.rooms

    def getPlayer(self):
        """
        Returns the Player object which the game creates
        """
        return self.player

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
        # Set directory path to narrative file
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "Narrative")
        os.chdir(dir)

        # Open title screen file and print title screen
        with open("../Narrative/titleScreen.txt") as titleFile:
            for line in titleFile.readlines():
                print(line.rstrip())

    def selectGameState(self):
        """
        Prompts the user to select a new game or load a saved game.
        """
        while True:
            # print message to input new game or load game
            print("Enter 'New' to start a new game or 'Load' to load a saved game:")
            userInput = input("> ")
            if userInput.replace(" ", "").lower() == "new":
                self.newGameIntro()
                return  # Default game state is new game
            if userInput.replace(" ", "").lower() == "load":
                print("!!! UNDER CONSTRUCTION !!!")
                # TODO::
                # print names of available saveSates (not default state)
                # take input for selected save and load corresponding saveState
            else:
                print("That's not a valid option.")

    def newGameIntro(self):
        """
        Displays introduction at the start of a new game.
        """
        # Set directory path to narrative file
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "Narrative")
        os.chdir(dir)

        # Open narrative file and print new game intro
        with open("../Narrative/newGameIntro.txt") as introFile:
            lineCount = 0
            for line in introFile.readlines():
                print(line.rstrip())
                lineCount += 1
                if lineCount in [5, 10, 16]:
                    time.sleep(1)
        print("(Enter the command 'exit game' to stop playing.)")
        print("(Enter 'help' at any time during the game for assistance.)")

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

    def buildItems(self):
        """
        Builds the items and loads them into the correct rooms
        """
        with open("Items/defaultLocations.json") as f:
            itemDict = json.load(f)
        f.close()
        for key, value in itemDict.items():
            itemName = key + ".json"
            file = os.path.join("Items", itemName)
            if type(value) == list:
                item = Item(file)
                for room in self.rooms:
                    if room == value[0]:
                        room.addItem(item)
                value = value[1]
            item = Item(file)
            for room in self.rooms:
                if room == value:
                    room.addItem(item)

    def setStartRoom(self):
        """
        This assigns the starting location of the Player
        """
        for room in self.rooms:
            if room.getName() == "masterBedroom":
                self.player.setLocation(room)
                return

    def printGameState(self):
        """
        Prints all Room and Player attributes to console for testing
        and debugging purposes.
        """
        print("------Current Player------")
        print("Location:", self.getPlayer().getLocation().getName())
        print("Inventory:", self.getPlayer().getInventory())
        print("------Current Rooms------")
        for room in self.getRooms():
            room.printRoomDetails()
            print("---")
