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

    def combineItems(self, otherItem):
        """This function is called when a player tries to use a different Item
        object with this Item object"""
        if self.itemInteractions[otherItem]:
            return self.itemInteractions[otherItem]
        else:
            return "Those items don't seem to work together"

    def verbResponses(self, verb):
        """This function is called when a player tries to perform an action on
        this Item object"""
        if self.verbInteractions[verb]:
            return self.verbInteractions[verb]
        else:
            return "I don't think that will work"