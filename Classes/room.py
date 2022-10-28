import json
from .conditional import Conditional as Cond


class Room:
    """
    This creates an instance of a room in the game
    """

    def __init__(self, roomFile):
        file = open(roomFile)

        # Load room data from JSON file
        data = json.load(file)

        # Basic room data
        self.name = data["name"]
        self.longDescription = data["longDescription"]
        self.shortDescription = data["shortDescription"]
        self.locked = False
        self.visited = False
        self.conditions = []

        # Add conditional items, if they exist for this room
        if "conditionalDescription" in data:
            for key, val in data["conditionalDescription"].items():
                name = key
                status = val["status"]
                trueDesc = data["conditionalDescription"][key]["True"]
                falseDesc = data["conditionalDescription"][key]["False"]
                self.conditions.append(Cond(name, status, trueDesc, falseDesc))

        # These variables are populated by the Game class
        self.exits = []
        self.items = []

        # Add features for the room, if they exist
        self.features = {}
        if "features" in data:
            for i in data["features"]:
                self.features[i] = data["features"][i]

        file.close()

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

    def getLongDescription(self):
        """
        Get full long description for a room
        """
        # The default long description
        desc = self.longDescription

        # Adds any conditional statements
        if self.conditions:
            desc = desc + " " + self.getConditionalDesc()

        # Describe any items that were left here by the player
        if self.items:
            desc = desc + self.getItemDescriptions()

        return desc

    def getShortDescription(self):
        """
        Get full short description for a room
        """
        # The default long description
        desc = self.shortDescription

        # Adds any conditional statements
        if self.conditions:
            desc = desc + self.getConditionalDesc()

        # Describe any items that were left here by the player
        if self.items:
            desc = desc + self.getItemDescriptions()

        return desc

    def getConditionalDesc(self):
        """
        Get current-state conditional descriptions for a room
        """
        tempStr = " "

        for index, item in enumerate(self.conditions):
            tempStr = tempStr + item.getDescription()

            # Add a space between additional items
            if index != len(self.conditions) - 1:
                tempStr = tempStr + " "

        return tempStr

    def getItemDescriptions(self):
        """
        This function will describe any items dropped in the room
        which do not normally belong here.
        """
        tempStr = " You left the "
        tempItems = self.items

        # Do not describe items that DO belong in this room by default
        for item in tempItems:
            for condition in self.conditions:
                if item.name == condition.name:
                    tempItems.remove(item)

        # Describe the ones that DON'T belong
        for index, item in enumerate(tempItems):
            tempStr = tempStr + item.name

            # Add a comma & space between additional items
            if index != len(tempItems) - 1:
                tempStr = tempStr + ", "

        tempStr = tempStr + " here."

        return tempStr

    def setCondition(self, name, boolVal):
        """
        Sets the status of a given conditional based on its name to True/False
        """
        for i in self.conditions:
            if i.name.lower() == name.lower():
                i.setStatus(boolVal)
                break

    def lock(self):
        """
        Locks the room
        """
        self.locked = True

    def unlock(self):
        """
        Unlocks the room
        """
        self.locked = False

    def isLocked(self):
        """
        Returns T/F if room is locked
        """
        return self.locked

    def setVisited(self):
        """
        Changes room from Unvisited to Visited
        """
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

    def removeItem(self, itemName):
        """
        Removes an item from the room - items are instances of Item class
        """
        for item in self.items:
            if item.name == itemName:
                self.items.remove(item)
                break

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
        print(f"######## Room name: {self.name} ########\n"
              f"- Locked? {self.locked}\n"
              f"- Visited? {self.visited}\n"
              f"- Long description:\n{self.getLongDescription()}\n"
              f"- Short description:\n{self.getShortDescription()}\n"
              f"- Conditionals:\n{self.getConditionalDesc()}\n"
              f"- Exits: {self.exits}\n"
              f"- Items: {self.items}")
        self.printDict("Features", self.features)
        print("")
