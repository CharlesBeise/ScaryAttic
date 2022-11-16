import json


class Item:
    """
    This creates an instance of a usable item in the game
    """

    def __init__(self, itemFile):
        """
        Initializes the necessary variables for the Item object
        """
        data = json.load(open(itemFile))
        self.name = data["name"]
        self.description = data["description"]
        self.secondaryDescription = data["secondaryDescription"]
        self.itemInteractions = data["itemInteractions"]
        self.verbInteractions = data["verbInteractions"]

    def getName(self):
        """
        This function returns the Item's name
        """
        return self.name

    def getDescription(self):
        """
        This function returns the Item description
        """
        return self.description

    def getSecondDescription(self):
        """
        This function returns the secondary description of the Item
        """
        return self.secondaryDescription

    def verbResponses(self, verb):
        """
        This function is called when a player tries to perform an action on
        this Item object
        """
        response = "I don't think that will work."
        try:
            response = self.verbInteractions[verb]
        except KeyError:
            pass
        return response

    def __eq__(self, other):
        """Checking a comparison"""
        if isinstance(other, str):
            return self.name.lower() == other.lower()
        return False
