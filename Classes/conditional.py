class Conditional:
    """
    Conditionals are used in Rooms, as anything that may change status.
    It takes the conditionalDescription JSON data from the
    Room where it is located.
    """
    def __init__(self, name, data):
        # Name the conditional
        self.name = name.lower()

        # Get its current (or default) status
        statusString = data["status"]
        self.status = True
        if statusString.lower() == "false":
            self.status = False

        # Get both possible descriptions
        self.trueDesc = data["true"]
        self.falseDesc = data["false"]

    def toggleStatus(self):
        """
        Toggle condition status between True/False
        """
        if self.status:
            self.status = False
        else:
            self.status = True

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
              f"   When true: {self.trueDesc}\n"
              f"   When false: {self.falseDesc}")