import json
import os
import pickle
import sys
import textwrap
import time
from .player import Player
from .room import Room
from .items import Item

# Minimum terminal height and width required to play
terminalMinHeight = 25
terminalMinWidth = 75


class Game:
    """
    Represents an instance of the game ScaryAttic.
    """
    def __init__(self) -> None:
        self.running = True
        self.saveFile = None
        self.rooms = []
        self.player = Player()
        self.itemStorage = []

        # Load help menu
        self.helpMenu = self.loadHelp()

        # Build instances of all the rooms
        self.buildRooms()
        self.buildItems()
        self.setStartRoom()

        # Win conditions
        self.foodInDish = False
        self.bellRung = False

    def getRooms(self):
        """
        Returns the list of Room objects in the current game.
        """
        return self.rooms

    def setRooms(self, rooms):
        """
        Assigns a list of Room objects to rooms in the game.
        """
        self.rooms = rooms

    def getPlayer(self):
        """
        Returns the Player object for the current game.
        """
        return self.player

    def setPlayer(self, player):
        """
        Assigns a Player object to the player of the game
        """
        self.player = player

    def getSaveFile(self):
        """
        Returns the name of the last file where the current game was saved.
        """
        return self.saveFile

    def setSaveFile(self, saveFile):
        """
        Assigns a file name to where the current game was last saved.
        """
        self.saveFile = saveFile

    def isRunning(self):
        """
        Returns True if Game is still being played or False if user
        has exited the game.
        """
        return self.running

    def checkForWin(self):
        """
        Checks if the game's win conditions have been met.
        Returns True/False.
        """
        if self.foodInDish and self.bellRung:
            return True
        return False

    def loadHelp(self):
        """
        Loads the help menu for the game.
        """
        helpString = ""
        with open("Narrative/helpMenu.txt") as helpFile:
            for line in helpFile.read().split('\n'):
                helpString = helpString + line + "\n"
        return helpString

    def printHelp(self):
        """
        Prints the help menu for the game.
        """
        print(self.helpMenu)

    def terminalSize(self):
        """
        Checks that the player terminal size is large enough to play
        the game. Notifies user and exits game if not large enough.
        """
        size = os.get_terminal_size()
        height, width = size[1], size[0]
        notification = (
            "This game must be played from a terminal.\n"
            "Your terminal window is not currently large enough.\nScary "
            f"Attic requires a minimum height of {terminalMinHeight} "
            f"(rows) and a minimum width of {terminalMinWidth} (columns)."
            f"\nYour current terminal has height of {height} and width of "
            f"{width}.\nPlease update the size of your terminal and "
            "restart the game to play.\n")
        if height < terminalMinHeight or width < terminalMinWidth:
            print(notification)
            sys.exit()

    def getImage(self, filename):
        """
        Returns ASCII art from a given file name.
        """
        with open("../Art/" + filename + ".txt") as imageFile:
            return imageFile.read()

    def titleScreen(self):
        """
        Displays game title screen.
        """
        self.terminalSize()  # Confirm terminal is large enough to play

        # Set directory path to narrative file
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "Narrative")
        os.chdir(dir)

        welcome = "Welcome to Scary Attic: A Text-Based Adventure Game!"
        credits = "Created by: Charles Beise, Andrew Blair, and Hannah Moon"
        titleImage = self.getImage("titleScreen")
        houseImage = self.getImage("introHouse")

        print(f"{houseImage}\n{titleImage}\n"
              f"          {welcome}\n        {credits}\n")

    def displayStartMessages(self):
        """
        Prints the long description for the room where the Player is
        currently located and offers instructions for playing.
        """
        print(self.getPlayer().getLocation().getLongDescription())
        print("\n(Enter the command 'exit game' to stop playing, "
              "or 'help' for assistance.)")

    def newGameIntro(self):
        """
        Displays introduction at the start of a new game.
        """
        print("")

        # Set directory path to narrative file
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "Narrative")
        os.chdir(dir)

        # Open narrative file and print new game intro
        with open("../Narrative/newGameIntro.txt") as introFile:
            for line in introFile.read().split('\n'):
                print(f"{textwrap.fill(line, terminalMinWidth)}\n")
                time.sleep(3)
        print("                                  *****\n")

        self.displayStartMessages()
        self.getPlayer().getLocation().setVisited()

    def triggerFoodCondition(self):
        """
        Triggers cat food win condition
        """
        self.foodInDish = True

    def triggerBellCondition(self):
        """
        Triggers silver bell win condition
        """
        self.bellRung = True

    def outro(self):
        """
        Displays the game's conclusion at the end.
        """
        print("")
        print("                                  *****\n")

        # Set directory path to narrative file
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "Narrative")
        os.chdir(dir)

        # Open narrative file and print new game intro
        with open("../Narrative/endGameOutro.txt") as introFile:
            for line in introFile.read().split('\n'):
                print(f"{textwrap.fill(line, terminalMinWidth)}\n")
                time.sleep(3)

        print("\n                    Thank you for playing Scary Attic.\n"
              "                    We sincerely hope you enjoyed it.\n\n"
              "                          S C A R Y A T T I C\n"
              "                          I T S A C A T C R Y\n\n")

    def getAllSavedGames(self):
        # Set directory path to save files
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "SaveFiles")
        savedGameFiles = os.listdir(dir)
        if ".gitignore" in savedGameFiles:
            savedGameFiles.remove(".gitignore")
        savedGameNames = []
        for file in savedGameFiles:
            fileParts = file.split(".")
            savedGameNames.append(fileParts[0])
        return savedGameNames

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
                if self.loadGame():
                    return
            else:
                print("That's not a valid option.")

    def pickleGameState(self, saveFileName):
        """
        Pickles the current state of all Rooms and the Player in the
        current Game. The pickled data is written to the specified
        save file.
        """
        saveFile = saveFileName + ".pickle"
        # Set directory path to save files
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "SaveFiles")
        os.chdir(dir)
        # Save game state to save file
        gameState = [self.rooms, self.player]
        with open(saveFile, "wb") as file:
            pickle.dump(gameState, file)

    def unpickleGameState(self, saveFileName):
        """
        Reads a save file and unpickles the state of all Rooms and the
        Player from the specified file.
        """
        saveFile = saveFileName + ".pickle"
        # Set directory path to save files
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "SaveFiles")
        os.chdir(dir)
        # Load game state from save file
        with open(saveFile, "rb") as file:
            gameState = pickle.load(file)
        return gameState

    def promptSaveFileName(self, savedGames):
        """
        Prompts the user to enter a file name where the current game will
        be saved. If the name exists, the user is asked to overwrite the
        existing file or enter a new file name.
        """
        fileChosen = False
        while not fileChosen:
            saveName = input("Please enter a file name where this game will be saved: ")
            if saveName in savedGames:
                print("This file already exists. Would you like to save over it?")
                saveOverInput = input("Y / N: ").replace(" ", "").lower()
                while saveOverInput not in ["y", "yes", "n", "no"]:
                    print("Your response was not valid. Would you like to save over the file?")
                    saveOverInput = input("Y / N: ").replace(" ", "").lower()
                if saveOverInput in ["y", "yes"]:
                    fileChosen = True
            else:
                fileChosen = True
        return saveName

    def saveGame(self):
        """
        Saves the current state of a Game to file.
        """
        savedGames = self.getAllSavedGames()
        currentSaveFile = self.getSaveFile()
        # If save files exist, print list of files
        if len(savedGames) > 0:
            print("These are the existing save files:")
            for file in savedGames:
                print("    ", file)
            if currentSaveFile:
                print("Your current game was last saved in", currentSaveFile)
        # Prompt user to enter a file name for saving
        currentSaveFile = self.promptSaveFileName(savedGames)
        self.setSaveFile(currentSaveFile)
        # Save the current game to file
        self.pickleGameState(currentSaveFile)
        print("Game save successful!")

    def loadGame(self):
        """
        Loads a Game state from file.
        """
        print("")

        fileChosen = False
        savedGames = self.getAllSavedGames()
        if len(savedGames) == 0:
            print("There are no saved games yet.")
            return False
        print("These are the existing save files:")
        for file in savedGames:
            print("    ", file)
        while not fileChosen:
            loadFile = input("Please enter which save file you want to load: ")
            if loadFile in savedGames:
                fileChosen = True
            else:
                print("That save file does not exist.")
        # Load the chosen game file
        loadedGame = self.unpickleGameState(loadFile)
        self.setRooms(loadedGame[0])
        self.setPlayer(loadedGame[1])
        self.setSaveFile(loadFile)
        print("\nGame load successful!\n")
        self.displayStartMessages()
        return True

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

        # Open the item's file
        for itemName, value in itemDict.items():
            itemPath = itemName + ".json"
            file = os.path.join("Items", itemPath)

            # Set location and visibility for this item
            location = value["location"]
            visible = False
            if value["visible"].lower() == "true":
                visible = True

            # Create an instance for each location
            for loc in location:
                item = Item(file)
                # Store it
                if loc == "storage":
                    self.itemStorage.append(item)
                    break
                for room in self.rooms:
                    if room == loc and visible:
                        room.addVisibleItem(item)
                        break
                    elif room == loc and not visible:
                        room.addHiddenItem(item)
                        break

    def setStartRoom(self):
        """
        This assigns the starting location of the Player
        """
        for room in self.rooms:
            if room.getName() == "masterBedroom":
                self.player.setLocation(room)
                return

    def addToItemStorage(self, item):
        """
        Adds an Item to game storage.
        """
        self.itemStorage.append(item)

    def removeFromItemStorage(self, itemName):
        """
        Take an item string name and tries to remove that item from storage.
        Returns the item if successful, False if not.
        """
        for item in self.itemStorage:
            if itemName == item.name:
                self.itemStorage.remove(item)
                return item
        return False

    def getAllAccessibleItems(self):
        """
        Retrieves a list including all accessible items from both the room
        and the player's inventory.
        """
        inventory = self.player.getInventory()
        room = self.player.getLocation().getAccessibleItems()
        return inventory + room

    def lockRoomByName(self, roomName):
        """
        Locks a room with the given name.
        Returns True if successful, False if not.
        """
        for room in self.rooms:
            if room == roomName:
                room.lock()
                return True
        return False

    def unlockRoomByName(self, roomName):
        """
        Unlocks a room with the given name.
        Returns True if successful, False if not.
        """
        for room in self.rooms:
            if room == roomName:
                room.unlock()
                return True
        return False

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
