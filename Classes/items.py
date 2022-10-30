import json


class Item:
    """This creates an instance of a usable item in the game"""

    def __init__(self, itemFile):
        """Initializes the necessary variables for the Item object"""
        itemLocation = "../Items/" + itemFile
        data = json.load(open(itemLocation))
        self.name = data["name"]
        self.description = data["description"]
        self.secondaryDescription = data["secondaryDescription"]
        self.itemInteractions = data["itemInteractions"]
        self.verbInteractions = data["verbInteractions"]

    def getName(self):
        """This function returns the Item's name"""
        return self.name

    def getDescription(self):
        """This function returns the Item description"""
        return self.description

    def getSecondDescription(self):
        """This function returns the secondary description of the Item"""
        return self.secondaryDescription

    def combineItems(self, otherItem):
        """This function is called when a player tries to use a different Item
        object with this Item object"""
        # TODO: I am still playing around with this. Will probably move it to
        #  the actionverbs file.
        if {self.name, otherItem.getName()} == {"flashlight", "battery"}:
            print("Here we are")
            return Item("flashlight3.json")
        if self.itemInteractions.get(otherItem):
            return self.itemInteractions[otherItem.getName()]
        else:
            return "Those items don't seem to work together"

    def verbResponses(self, verb):
        """This function is called when a player tries to perform an action on
        this Item object"""
        if self.verbInteractions[verb]:
            return self.verbInteractions[verb]
        else:
            return "I don't think that will work"

    def __eq__(self, other):
        """Checking a comparison"""
        if isinstance(other, str):
            return self.name.lower() == other.lower()
        return False
