class Player:
    """
    Represents a player of the game ScaryAttic.
    """
    def __init__(self) -> None:
        self.location = None
        self.inventory = []

    def getLocation(self):
        """
        Returns the Room (object) where the Player is currently located.
        """
        return self.location

    def getLocationByName(self):
        """
        Returns the name (string) of the Room where the Player is
        currently located.
        """
        return self.location.name

    def setLocation(self, room):
        """
        Updates the Room where the Player is currently located.
        """
        self.location = room

    def getInventory(self):
        """
        Returns a list of Items currently in the Player inventory.
        """
        return self.inventory

    def addInventory(self, item):
        """
        Adds an Item to the Player inventory and returns True if
        successful.
        """
        self.inventory.append(item)
        # self.inventory.sort()  # optional auto-sorting of inventory
        return True

    def removeInventory(self, item):
        """
        Removes an Item from the Player inventory and returns True if
        successful. Otherwise returns False.
        """
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        else:
            return False

    def hasFlashlight(self):
        """
        Returns True or False if player has a working flashlight.
        (Needs flashlight3: flashlight + both batteries)
        """
        if "flashlight3" in self.inventory:
            return True
        return False
