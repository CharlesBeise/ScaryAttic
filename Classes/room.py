import json
import textwrap
from .conditional import Conditional as Cond

fill_width = 75


class Room:
    """
    This creates an instance of a room in the game
    """

    def __init__(self, roomFile):
        file = open(roomFile, encoding="utf8")

        # Load room data from JSON file
        data = json.load(file)

        # Basic room data
        self.name = data["name"]
        self.longDescription = data["longDescription"]
        self.shortDescription = data["shortDescription"]
        self.verbInteractions = data["verbInteractions"]
        self.locked = False
        self.visited = False
        self.conditions = []
        self.exits = {}

        # Add conditional items, if they exist for this room
        if "conditionalDescription" in data:
            for key, val in data["conditionalDescription"].items():
                name = key
                try:
                    status = val["status"]
                    trueDesc = val["True"]
                    falseDesc = val["False"]
                except KeyError:
                    status = ""
                    trueDesc = ""
                    falseDesc = ""
                self.conditions.append(Cond(name, status, trueDesc, falseDesc))

        # Add room exits
        for key, val in data["exits"].items():
            self.exits[key] = val

        # Dropped Items are things dropped by the player during gameplay,
        # whether the item originally belonged in the room or not.
        self.droppedItems = []

        # Unlocked Items belong in the room by default,
        # but are VISIBLE and ACCESSIBLE to the player.
        self.visibleItems = []

        # Hidden Items belong in the room by default,
        # but they are INVISIBLE and INACCESSIBLE to the player.
        self.hiddenItems = []

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
            desc = desc + self.getConditionalDesc()

        # Describe any items that were left here by the player
        if self.droppedItems:
            desc = desc + self.getItemDescriptions()

        return textwrap.fill(desc, fill_width)

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
        if self.droppedItems:
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
        This function will describe any items dropped in the room.
        """
        tempStr = " You left the "

        for index, item in enumerate(self.droppedItems):
            tempStr = tempStr + item.name

            # Add a comma & space between additional items
            if index != len(self.droppedItems) - 1:
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

    def getAllExits(self):
        """
        Returns full exits data
        """
        return self.exits

    def isValidExit(self, exit):
        """
        Input a room name OR direction string, and a boolean value is returned.
        Input parameter is case-insensitive and spaces are irrelevant.
        """
        toFind = exit.replace(" ", "").lower()

        for key, val in self.exits.items():
            shortKey = key.replace(" ", "").lower()
            shortVal = val.replace(" ", "").lower()
            if toFind == shortKey or toFind == shortVal:
                return True
        return False

    def addDroppedItem(self, item):
        """
        Adds a dropped item to the room.
        This should be used when the player "drops" items.
        Input "item" should be Item object.
        """
        self.droppedItems.append(item)

    def removeDroppedItem(self, itemName):
        """
        Removes a dropped item from the room.
        This should be used when the player "picks up" a dropped item.
        Input "itemName" should be an item's name string.
        Returns the item if removed, or 1 if item wasn't found.
        """
        for item in self.droppedItems:
            if item.name == itemName:
                self.droppedItems.remove(item)
                return item
        return 1

    def getDroppedItems(self):
        """
        Returns the list of items dropped in the room.
        Does NOT include items which are in their default locations.
        """
        return self.droppedItems

    def addHiddenItem(self, item):
        """
        Adds a hidden item to the room.
        This should be used when the Game class builds the items.
        Input "item" should be Item object.
        """
        self.hiddenItems.append(item)

    def removeHiddenItem(self, itemName):
        """
        Removes a hidden item from the room.
        Input "itemName" should be an item's name string.
        Returns the item if removed, or 1 if item wasn't found.
        """
        for item in self.hiddenItems:
            if item.name == itemName:
                self.hiddenItems.remove(item)
                return item
        return 1

    def getHiddenItems(self):
        """
        Returns the list of hidden items in the room.
        """
        return self.hiddenItems

    def addVisibleItem(self, item):
        """
        Adds a visible item to the room.
        Input "item" should be Item object.
        """
        self.visibleItems.append(item)

    def removeVisibleItem(self, itemName):
        """
        Removes a visible item from the room.
        Input "itemName" should be an item's name string.
        Returns the item if removed, or 1 if item wasn't found.
        """
        for item in self.visibleItems:
            if item.name == itemName:
                self.visibleItems.remove(item)
                return item
        return 1

    def getVisibleItems(self):
        """
        Returns the list of visible items in the room.
        """
        return self.visibleItems

    def unlockItem(self, itemName):
        """
        Switches an item from hidden to visible.
        Input "itemName" should be an item's name string.
        """
        for item in self.hiddenItems:
            if item.name == itemName:
                self.addVisibleItem(item)
                self.removeHiddenItem(item)

    def isItemLocked(self, itemName):
        """
        Returns boolean for whether an item is accessible by the player or not.
        Input "itemName" should be an item's name string.
        """
        for item in self.getAccessibleItems():
            if item.name == itemName:
                return False
            else:
                return True

    def getAccessibleItems(self):
        """
        Returns the list of all items in the room which are
        visible and accessible to the player. Includes both
        dropped and visible room items.
        """
        return self.droppedItems + self.visibleItems

    def removeAccessibleItem(self, itemName):
        """
        Removes a visible item from the room.
        This can be used for moving an item from the room to the inventory.
        Input "itemName" should be an item's name string.
        Returns the item if removed, or 1 if item wasn't found.
        """
        # Check visible items
        result = self.removeVisibleItem(itemName)
        if result == 1:
            result = self.removeDroppedItem(itemName)
            if result == 1:
                # If it's on neither list, return 1
                return 1
        return result

    def verbResponses(self, verb, feature):
        """
        This function is called when a player tries to perform an action on
        this Item object
        """
        response = "I don't think that will work."
        try:
            response = self.verbInteractions[verb][feature]
        except KeyError:
            pass
        return response

    # TODO: Add method for applicable verb actions?

    # TODO: The following two functions can be removed later, if desired.

    def printDict(self, dictName, thisDict):
        """
        Prints a 'pretty' version of a dict
        """
        print(f"- {dictName}:")
        for i in thisDict:
            print(f"{i} - {thisDict[i]}")

    def printConditionalsTest(self):
        """
        Returns details of this room's conditional descriptions.
        """
        tempStr = ""
        index = 1

        for i in self.conditions:
            tempStr = tempStr + str(index) + ". Name: '" + i.name + \
                "'\n   When true: " + i.trueDesc + \
                "\n   When false: " + i.falseDesc + "\n"
            index = index + 1

        return tempStr

    def printRoomDetails(self):
        """
        Prints room details for easier debugging
        """
        dropItems = ""
        hidItems = ""
        visItems = ""

        if self.droppedItems:
            for d in self.droppedItems:
                dropItems = dropItems + d.name + ", "

        if self.hiddenItems:
            for h in self.hiddenItems:
                hidItems = hidItems + h.name + ", "

        if self.visibleItems:
            for v in self.visibleItems:
                visItems = visItems + v.name + ", "

        print(f"######## Room name: {self.name} ########\n"
              f"- Locked? {self.locked}\n"
              f"- Visited? {self.visited}\n"
              f"- Long description:\n{self.getLongDescription()}\n"
              f"- Short description:\n{self.getShortDescription()}\n"
              f"- Exits: {self.exits}\n"
              f"- Hidden items: {hidItems[:-2]}\n"
              f"- Visible items: {visItems[:-2]}\n"
              f"- Dropped items: {dropItems[:-2]}\n"
              f"- Conditionals:\n{self.printConditionalsTest()}")
        print("")
