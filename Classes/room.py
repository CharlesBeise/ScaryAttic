import json

# Room class for the various rooms of the house
# Each room will be an instance of the Room class

class Room:
    def __init__(self, jsonData):
        # Load room data from JSON file
        # print(f"\n!!! New room created from file: {jsonData} !!!")
        data = json.load(open(jsonData))

        # Basic room data
        self.name = data["name"]
        self.longDescription = data["longDescription"]
        self.longDescription = data["longDescription"]
        self.shortDescription = data["shortDescription"]
        self.locked = False
        self.visited = False

        # Conditions list contains a set of Boolean values.
        # These conditions are used to toggle settings in each room.
        #
        # Each condition variable should be matched with TWO
        # conditional Descriptions in the condDescr dict,
        # in the SAME ORDER.
        #
        # Conditional descriptions should be formatted as follows:
        # True case first, False case second
        self.conditions = []
        self.condDescr = []

        # Add conditional descriptions, if they exist
        if "conditionalDescription" in data:
            for i in data["conditionalDescription"]:
                self.condDescr.append(data["conditionalDescription"][i])

        # Set up conditionals depending on this room
        # TODO: These will need to be filled out for each room
        if self.name.lower() == "garage":
            self.conditions.append(True)    # Ladder exists or not
            self.conditions.append(False)   # Garage door is open or not

        # These variables are populated by the Game class
        self.exits = {}
        self.items = []

        # Add features for the room, if they exist
        self.features = {}
        if "features" in data:
            for i in data["features"]:
                self.features[i] = data["features"][i]

        # self.printRoomDetails()

    # This method allows the Room instance to equal its name
    # when compared to a String. It is case-insensitive.
    def __eq__(self, other):
        if isinstance(other, str):
            return self.name.lower() == other.lower()
        else:
            return False

    # Returns the room's Name
    def getName(self):
        return self.name

    # Changes the room's Name
    def setName(self, name):
        self.name = name

    # Get full long description for a room
    def getLongDescription(self):
        # index for the conditional descriptions
        index = 0

        # The default long description
        desc = self.longDescription

        # Adds any conditional statements
        if self.conditions:
            for thisCondition in self.conditions:
                if thisCondition:
                    desc = desc + " " + self.condDescr[index]
                else:
                    desc = desc + " " + self.condDescr[index + 1]
                index = index + 2

        # TODO: Describe any items that were left here by the player

        return desc

    # Get full short description for a room
    def getShortDescription(self):
        # index for the conditional descriptions
        index = 0

        # The default long description
        desc = self.shortDescription

        # Adds any conditional statements
        if self.conditions:
            for thisCondition in self.conditions:
                if thisCondition:
                    desc = desc + " " + self.condDescr[index]
                else:
                    desc = desc + " " + self.condDescr[index + 1]
                index = index + 2

        # TODO: Describe any items that were left here by the player

        return desc
    
    # Switch value of a given conditional variable
    def toggleCondition(self, index):
        if self.conditions[index]:
            self.conditions[index] = False
        else:
            self.conditions[index] = True

    # Switches the 'locked' status of the room
    def toggleLock(self):
        if self.locked:
            self.locked = False
        else:
            self.locked = True

    # Returns T/F if room is locked
    def isLocked(self):
        return self.locked

    # Switches the 'visited' status of the room
    def toggleVisited(self):
        if self.visited:
            self.visited = False
        else:
            self.visited = True

    # Returns T/F if the room has been visited
    def isVisited(self):
        return self.visited

    # Adds an exit to this room - exits will be instances of Room class
    def addExit(self, roomName, exitDirection):
        self.exits[roomName] = exitDirection

    # Adds an item to the room - items will be instances of Item class
    def addItem(self, item):
        self.items.append(item)

    # TODO: Add method for applicable verb actions?

    # The following two functions can be removed later, if desired.

    # Prints a 'pretty' version of a dict
    def printDict(self, dictName, thisDict):
        print(f"- {dictName}:")
        for i in thisDict:
            print(f"{i} - {thisDict[i]}")

    # Prints room details for easier debugging
    def printRoomDetails(self):
        print(f"- Name: {self.name}\n"
              f"- Locked? {self.locked}\n"
              f"- Visited? {self.visited}\n"
              f"- Long description:\n{self.getLongDescription()}\n"
              f"- Short description:\n{self.getShortDescription()}\n"
              f"- Exits: {self.exits}\n"
              f"- Items: {self.items}")
        self.printDict("Features", self.features)
        print("")
