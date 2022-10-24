class Conditional:
    """
    Conditionals are used in Rooms, as anything that may change status.
    It takes the conditionalDescription JSON data from the
    Room where it is located.

    Data parameter is a dict of conditional descriptions from Room.
    """
    def __init__(self, name, status, dataDict):
        # Name the conditional
        self.name = name.lower()

        # Get its current (or default) status
        statusString = status
        self.status = True
        if statusString.lower() == "false":
            self.status = False

        # Get both possible descriptions
        self.trueDesc = dataDict["true"]
        self.falseDesc = dataDict["false"]

        self.printConditional()

    def getStatus(self):
        """
        Returns the Boolean status of this condition
        """
        return self.status

    def setStatus(self, status):
        """
        Set status to True or False
        """
        self.status = status

    def getName(self):
        """
        Get the name of this conditional
        """
        return self.name

    def getDescription(self):
        """
        Get description based on conditional's status
        """
        if self.status:
            return self.trueDesc
        else:
            return self.falseDesc

    def printConditional(self):
        """
        Print details of this conditional for debugging
        """
        print(f"Conditional name: {self.name}\n"
              f"   Status: {self.status}\n"
              f"   When true: {self.trueDesc}\n"
              f"   When false: {self.falseDesc}")
