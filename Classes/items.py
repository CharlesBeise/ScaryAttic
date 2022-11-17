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

        # Items without ASCII art are just assigned an empty string
        self.image = ""
        if "polaroid" in self.name:
            self.image = self.readImageFromFile()
            print(f"Image for {self.name}:\n{self.image}")

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
        if self.image != "":
            return self.image + "\n" + self.description
        else:
            return self.description

    def getSecondDescription(self):
        """
        This function returns the secondary description of the Item
        """
        return self.secondaryDescription

    def combineItems(self, otherItem):
        """
        This function is called when a player tries to use a different Item
        object with this Item object
        """
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

    def getImage(self):
        """
        This function returns the item's ASCII art string, when applicable
        """
        return self.image

    def readImageFromFile(self):
        """
        Gets ASCII art for this item from file and saves it to
        the image attribute. Returns the image as a string.
        """
        with open("Art/" + self.name + ".txt") as imageFile:
            image = imageFile.read()
            return image

    def __eq__(self, other):
        """Checking a comparison"""
        if isinstance(other, str):
            return self.name.lower() == other.lower()
        return False
