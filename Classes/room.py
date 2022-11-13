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

        # Set certain rooms to be locked by default
        if data["lockRoom"] == "True":
            self.locked = True

        # Add conditional items, if they exist for this room
        if "conditionals" in data:
            for key, val in data["conditionals"].items():
                try:
                    names = val['triggerSequence']
                    loop = val['loop']
                    descriptions = []

                    # Get all step descriptions
                    for i in range(len(val) - 2):
                        descriptions.append(val[str(i)])
                except (KeyError, ValueError):
                    print(
                        f"Error building room conditionals: '{self.name}'")
                    names = []
                    loop = ""
                    descriptions = []

                self.conditions.append(Cond(names, loop, descriptions))

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

        return textwrap.fill(desc, fill_width)

    def getConditionalDesc(self):
        """
        Get current-state conditional descriptions for a room
        """
        tempStr = " "

        for index, condition in enumerate(self.conditions):
            # Empty descriptions will be skipped
            if condition.getDescription() != "":
                tempStr = tempStr + condition.getDescription()

                # Add a separator between any additional items
                if index != len(self.conditions) - 1:
                    tempStr = tempStr + " "

        return tempStr

    def getItemDescriptions(self):
        """
        This function will describe any items dropped in the room
        which do not normally belong here.
        """
        tempStr = " You left the "

        for index, item in enumerate(self.droppedItems):
            tempStr = tempStr + item.name

            # Add a comma & space between additional items
            if index != len(self.droppedItems) - 1:
                tempStr = tempStr + ", "

        tempStr = tempStr + " here."

        return tempStr

    def triggerCondition(self, name):
        """
        Call this method to move a named condition to its next step.
        Input "name" should be a string for the condition being triggered.
        """
        condName = name.lower()
        conditionFound = False

        # If the condition matches one of our conditions, try to trigger it
        for condition in self.conditions:
            # print(f"Does condName '{condName}' == trigger '{condition.trigger}'?")
            if condName == condition.trigger:
                # print("It does.")
                condition.triggerCondition(condName)
                conditionFound = True
                break

        # Unlocks items when necessary
        if conditionFound:
            if self.name == "masterBedroom" and "box" in condName:
                self.unlockItem("battery")

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
        Returns the item if removed, or None if item wasn't found.
        """
        for item in self.droppedItems:
            if item.name == itemName:
                self.droppedItems.remove(item)
                return item
        return None

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
        Returns the item if removed, or None if item wasn't found.
        """
        for item in self.hiddenItems:
            if item.name == itemName:
                self.hiddenItems.remove(item)
                return item
        return None

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
        Returns the item if removed, or None if item wasn't found.
        """
        for item in self.visibleItems:
            if item.name == itemName:
                self.visibleItems.remove(item)
                return item
        return None

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
        Returns the item if removed, or None if item wasn't found.
        """
        # Check visible items
        result = self.removeVisibleItem(itemName)
        if result is None:
            result = self.removeDroppedItem(itemName)
            if result is None:
                # If it's on neither list, return None
                return None
        return result

    def verbResponses(self, verb, feature):
        """
        This function is called when a player tries to perform an action on
        this Item object
        """
        response = "I'm not sure what you mean. Try something else."
        try:
            response = self.verbInteractions[verb][feature]
            self.triggerCondition(feature)
        except KeyError:
            pass
        return textwrap.fill(response, fill_width)

    # TODO: The following function can be removed later, if desired.

    def printRoomDetails(self):
        """
        Prints room details for easier debugging
        """

        dropItems = ""
        hidItems = ""
        visItems = ""
        conditions = ""

        if self.droppedItems:
            for d in self.droppedItems:
                dropItems = dropItems + d.name + ", "

        if self.hiddenItems:
            for h in self.hiddenItems:
                hidItems = hidItems + h.name + ", "

        if self.visibleItems:
            for v in self.visibleItems:
                visItems = visItems + v.name + ", "

        if self.conditions:
            for c in self.conditions:
                for name in c.names:
                    conditions = conditions + name + ", "

        print(f"######## Room name: {self.name} ########\n"
              f"- Locked? {self.locked}\n"
              f"- Visited? {self.visited}\n"
              f"- Long description:\n{self.getLongDescription()}\n"
              f"- Short description:\n{self.getShortDescription()}\n"
              f"- Exits: {self.exits}\n"
              f"- Hidden items: {hidItems[:-2]}\n"
              f"- Visible items: {visItems[:-2]}\n"
              f"- Dropped items: {dropItems[:-2]}\n"
              f"- Condition triggers: {conditions[:-2]}")
        print("")
