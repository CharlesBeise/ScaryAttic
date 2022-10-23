import json
from .conditional import Conditional as Cond


class Room:
    """
    This creates an instance of a room in the game
    """

    def __init__(self, roomFile):
        # Load room data from JSON file
        # print(f"\n!!! New room created from file: {roomFile} !!!")
        data = json.load(open(roomFile))

        # Basic room data
        self.name = data["name"]
        self.longDescription = data["longDescription"]
        self.shortDescription = data["shortDescription"]
        self.locked = False
        self.visited = False
        self.conditions = []

        # Add conditional items, if they exist for this room
        if "conditionalDescription" in data:
            for i in data["conditionalDescription"]:
                info = data["conditionalDescription"][i]
                self.conditions.append(Cond(i, info))

        # These variables are populated by the Game class
        self.exits = {}
        self.items = []

        # Add features for the room, if they exist
        self.features = {}
        if "features" in data:
            for i in data["features"]:
                self.features[i] = data["features"][i]

        # self.printRoomDetails()

    def __eq__(self, other):
        """
        This method allows the Room instance to equal its name when
        compared to a String. It is case-insensitive.
        """
        if isinstance(other, str):
            return self.name.lower() == other.lower()
        else:
            return False

    def getName(self):
        """
        Returns the room's Name
        """
        return self.name

    def setName(self, name):
        """
        Changes the room's Name
        """
        self.name = name

    def getLongDescription(self):
        """
        Get full long description for a room
        """
        # The default long description
        desc = self.longDescription

        # Adds any conditional statements

        # TODO: Describe any items that were left here by the player

        return desc

    def getShortDescription(self):
        """
        Get full short description for a room
        """
        # The default long description
        desc = self.shortDescription

        # Adds any conditional statements

        # TODO: Describe any items that were left here by the player

        return desc

    def getConditionals(self):
        """
        Get current-state conditional descriptions for a room
        """
        tempStr = ""

        for index, item in enumerate(self.conditions):
            tempStr = tempStr + item.getDescription()

            # Add a space between additional items
            if index != len(self.conditions) - 1:
                tempStr = tempStr + " "

        return tempStr

    def toggleConditional(self, name):
        """
        Toggle the state of a given conditional based on its name
        """
        for i in self.conditions:
            if i.name.lower() == name.lower():
                i.toggleStatus()
                break

    def toggleLock(self):
        """
        Switches the 'locked' status of the room
        """
        if self.locked:
            self.locked = False
        else:
            self.locked = True

    def isLocked(self):
        """
        Returns T/F if room is locked
        """
        return self.locked

    def toggleVisited(self):
        """
        Switches the 'visited' status of the room
        """
        if self.visited:
            self.visited = False
        else:
            self.visited = True

    def isVisited(self):
        """
        Returns T/F if the room has been visited
        """
        return self.visited

    def addExit(self, roomName, exitDirection):
        """
        Adds an exit to this room - exits will be instances of Room class
        """
        self.exits[roomName] = exitDirection

    def addItem(self, item):
        """
        Adds an item to the room - items will be instances of Item class
        """
        self.items.append(item)

    # TODO: Add method for applicable verb actions?

    # TODO: The following two functions can be removed later, if desired.

    def printDict(self, dictName, thisDict):
        """
        Prints a 'pretty' version of a dict
        """
        print(f"- {dictName}:")
        for i in thisDict:
            print(f"{i} - {thisDict[i]}")

    def printRoomDetails(self):
        """
        Prints room details for easier debugging
        """
        print(f"- Name: {self.name}\n"
              f"- Locked? {self.locked}\n"
              f"- Visited? {self.visited}\n"
              f"- Long description:\n{self.getLongDescription()}\n"
              f"- Short description:\n{self.getShortDescription()}\n"
              f"- Conditionals:\n{self.getConditionals()}\n"
              f"- Exits: {self.exits}\n"
              f"- Items: {self.items}")
        self.printDict("Features", self.features)
        print("")
