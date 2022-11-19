import json
import textwrap
from .conditional import Conditional as Cond

fillWidth = 75


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
                    name = key
                    seq = val['triggerSequence']
                    verbs = val['triggerVerbs']
                    loop = val['loop']
                    type = val['type']
                    descriptions = []

                    # Get all step descriptions
                    for i in range(len(val) - 4):
                        descriptions.append(val[str(i)])
                except (KeyError, ValueError):
                    print(
                        f"Error building room conditionals: '{self.name}'")
                    name, seq, verbs, loop, type, descriptions = "", [], [], \
                                                                 "", "", []

                self.conditions.append(Cond(
                    name,
                    seq,
                    verbs,
                    loop,
                    type,
                    descriptions))

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

        return textwrap.fill(desc, fillWidth, replace_whitespace=False)

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

        return textwrap.fill(desc, fillWidth, replace_whitespace=False)

    def getConditionalDesc(self):
        """
        Get current-state conditional descriptions for a room.
        Only includes conditions of the "room" type.
        """
        tempStr = " "

        for index, condition in enumerate(self.conditions):
            # Empty descriptions will be skipped
            if condition.getDescription() != "" and condition.type == "room":
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
        tempStr = "You left the "

        for index, item in enumerate(self.droppedItems):
            tempStr = tempStr + item.name
            listLen = len(self.droppedItems)

            # Add comma/space between additional items
            if listLen == 2 and index == 0:
                tempStr = tempStr + " and "
            elif index != listLen - 1:
                sep = ", "
                if listLen > 2 and index == listLen - 2:
                    sep = ", and "
                tempStr = tempStr + sep

        tempStr = tempStr + " here."

        return tempStr

    def triggerConditionRoom(self, name, verb):
        """
        Call this method to move a named condition to its next step.
        Input "name" should be a string for the condition being triggered.
        """
        conditionFound = False

        # If the condition matches one of our conditions, try to trigger it
        for condition in self.conditions:
            if name == condition.trigger and verb in condition.triggerVerbs:
                if condition.triggerCondition(name):
                    conditionFound = True

        # This small block of code is a work in progress and will
        # probably change later...
        # Unlocks items when necessary
        if conditionFound:
            self.checkUnlock(name, verb)

    def checkUnlock(self, name, verb):
        """
        Temporary way of unlocking items
        """
        if self.name == "masterBedroom" and "box" in name:
            self.unlockItem("battery")
        elif self.name == "utilityRoom" and "shelves" in name:
            self.unlockItem("flashlight")
        elif self.name == "secondBedroom" and "box" in name:
            self.unlockItem("battery")
        elif self.name == "upperHall" and "painting" in name and verb in \
                ["Shake", "Flip", "Peel"]:
            self.unlockItem("polaroid1")
        elif self.name == "kitchen" and "drawer" in name:
            self.unlockItem("canOpener")
        elif self.name == "kitchen" and "cabinet" in name:
            self.unlockItem("polaroid2")

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
        return result

    def verbResponses(self, verb, feature, trigger=True):
        """
        This function is called when a player tries to perform an action on
        this Item object
        """
        try:
            response = self.verbInteractions[verb][feature]
        except KeyError:
            response = None

        # Conditional responses have to be retrieved from conditions
        if response == "conditional":
            # Look for the condition and get its current description
            for cond in self.conditions:
                # Only the specified verbs are allowed to get the next
                # description, however "Examine" is always able to get the
                # description
                if cond.name == feature and \
                        (verb == "Examine" or verb in cond.triggerVerbs):
                    response = cond.getDescription()

        # Trigger any conditions with this interaction.
        # If there is no valid trigger, this should do nothing.
        if trigger:
            self.triggerConditionRoom(feature, verb)

        # Failure or empty descriptions provide an error
        if response is None or response == "" or response == "conditional":
            response = "I'm not sure what you mean. Try something else."

        return textwrap.fill(response, fillWidth)

    # TODO: The following function can be removed later, if desired.

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
              f"- Dropped items: {dropItems[:-2]}\n")
        print("")
