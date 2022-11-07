import json
import os
import pickle
import time
from .player import Player
from .room import Room
from .items import Item


class Game:
    """
    Represents an instance of the game ScaryAttic.
    """
    def __init__(self) -> None:
        self.running = True
        self.saveFile = None
        self.rooms = []
        self.player = Player()

        # Build instances of all the rooms
        self.buildRooms()
        self.buildItems()
        self.setStartRoom()

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

    def getAllSavedGames(self):
        # Set directory path to save files
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "SaveFiles")
        savedGames = os.listdir(dir)
        if ".gitignore" in savedGames:
            savedGames.remove(".gitignore")
        for file in savedGames:
            file = file.split(".")[0]
        return savedGames

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

    def pickleGameState(self, saveFile):
        """
        Pickles the current state of all Rooms and the Player in the
        current Game. The pickled data is written to the specified
        save file.
        """
        saveFile = saveFile + ".pickle"
        # Set directory path to save files
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "SaveFiles")
        os.chdir(dir)
        # Save game state to save file
        gameState = [self.rooms, self.player]
        with open(saveFile, "wb") as file:
            pickle.dump(gameState, file)

    def unpickleGameState(self, savefile):
        """
        Reads a save file and unpickles the state of all Rooms and the
        Player from the specified file.
        """
        saveFile = saveFile + ".pickle"
        # Set directory path to save files
        path = os.path.realpath(__file__)
        dir = os.path.dirname(path)
        dir = dir.replace("Classes", "SaveFiles")
        os.chdir(dir)
        # Load game state from save file
        with open(savefile, "rb") as file:
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
        print("Game load successful!")

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
