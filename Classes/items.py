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
        self.inventoryName = data["inventoryName"]
        self.description = data["description"]
        self.secondaryDescription = data["secondaryDescription"]
        self.itemInteractions = data["itemInteractions"]
        self.verbInteractions = data["verbInteractions"]

        # Items without ASCII art are just assigned an empty string
        self.images = {}
        if "polaroid" in self.name:
            frontImage = self.readImageFromFile(self.name)
            backImage = self.readImageFromFile(self.name + "back")
            self.images["front"] = frontImage
            self.images["back"] = backImage

    def getName(self):
        """
        This function returns the Item's name
        """
        return self.name

    def getInventoryName(self):
        """
        This function returns the name to be used for the Item in the player's
        inventory
        """
        return self.inventoryName

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

    def getImage(self, imageName):
        """
        This function returns the item's ASCII art string, when applicable
        """
        return self.images[imageName]

    def readImageFromFile(self, fileName):
        """
        Gets ASCII art for this item from file and saves it to
        the image attribute. Returns the image as a string.
        """
        with open("Art/" + fileName + ".txt") as imageFile:
            image = imageFile.read()
            return image

    def getItemInteraction(self, itemName):
        """
        Retrieves a formatted description from the specified
        item interaction.
        """
        return self.itemInteractions[itemName]

    def getVerbInteraction(self, verb):
        """
        Retrieves a formatted description from the specified
        item interaction.
        """
        return self.verbInteractions[verb]

    def __eq__(self, other):
        """Checking a comparison"""
        if isinstance(other, str):
            return self.name.lower() == other.lower() or \
                   self.inventoryName.lower() == other.lower()
        return False
