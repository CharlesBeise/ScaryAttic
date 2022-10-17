# Room class for the various rooms of the house
# Each room will be an instance of the Room class

class Room:
    name = ""
    locked = False
    visited = False
    longDescription = ""
    shortDescription = ""
    conditionalDescriptions = {}
    exits = {}
    items = []
    features = {}

    def __init__(self, fileInput):
        # TODO: Read room's information from JSON file
        # Get name, descriptions, items, etc from the JSON file
        # in Rooms folder, which has default NEW GAME information.

        print(f"New room created from file: {fileInput}")

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def toggleLock(self):
        if self.locked:
            self.locked = False
        else:
            self.locked = True

    def isLocked(self):
        return self.locked

    def toggleVisited(self):
        if self.visited:
            self.visited = False
        else:
            self.visited = True

    def isVisited(self):
        return self.visited

    def addExit(self, roomName, exitDirection):
        self.exits[roomName] = exitDirection

    def addItem(self, item):
        self.items.append(item)

    # TODO: Add applicable verb actions?
    # TODO: Add features
    # TODO: Should Game class handle tracking of item location, or the rooms?
