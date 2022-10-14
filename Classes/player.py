class Player:
    """
    Represents a player of the game ScaryAttic
    """
    def __init__(self) -> None:
        self.location = None
        self.inventory = []
        pass

    def getLocation(self):
        """Returns the room where the Player is currently located"""
        return self.location

    def setLocation(self, room):
        """Updates the room where the Player is currently located"""
        self.location = room

    def getInventory(self):
        """Returns a list of Items currently in the Player inventory"""
        return self.inventory

    def addInventory(self, item):
        """Adds an item to the Player inventory and sorts inventory"""
        self.inventory.append(item)
        self.inventory.sort()
        return True

    def removeInventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        else:
            return False
