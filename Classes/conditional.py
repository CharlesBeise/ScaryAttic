class Conditional:
    """
    Conditionals are used in Rooms, as anything that may change status.
    It takes the "conditions" JSON data from the
    Room where it is located.

    Input "name" as String for this condition.
    Input "loop" expects a string reading "True" or "False".
    Input "descriptions" takes a list of descriptions per step.
    """
    def __init__(self, names, loop, descriptions):
        # Names contains a sequence of all trigger words for this condition
        self.names = names

        # Attribute "trigger" is the current name of this condition,
        # which is required to proceed to the next step.
        self.trigger = self.names[0]

        # Loop attribute determines if this is a condition that can
        # toggle back and forth (True) or if it only progresses forward (False)
        if loop.lower() == "true" or loop is True:
            self.loop = True
        else:
            self.loop = False

        # Initialize current state of the condition
        self.currentStep = 0

        # Get total number of steps for this condition
        self.totalSteps = len(descriptions)

        # A list of all descriptions for this item's various states
        self.descriptions = descriptions

    def __eq__(self, other):
        """
        This method allows the Condition instance to its current trigger
        when compared to a String.
        """
        if isinstance(other, str):
            if other.lower() == self.trigger:
                return True
        else:
            return False

    def triggerCondition(self, trigger):
        """
        Increments current state by one step.
        Use this to move the condition's progress forward.

        Returns 0 if successful.
        Returns 1 otherwise.
        """
        # If needed, increment to the next trigger
        self.nextTrigger()

        # print(f"Incrementing to condition: {self.trigger}")

        # If this condition loops, it will go back around to step 0 at the
        # end of its steps
        if self.loop and self.currentStep == (self.totalSteps - 1):
            self.currentStep = 0
            return 0
        # Conditions that do not loop will STOP at the end of their steps
        elif not self.loop and self.currentStep == (self.totalSteps - 1):
            return 0
        # All other cases increment normally
        else:
            self.currentStep += 1

    def nextTrigger(self):
        """
        This function increments the trigger word for the condition.
        Returns 0 for success, or 1 for failure.
        """
        # If there are more triggers in line, set the next trigger
        if self.trigger != self.names[-1]:
            # print(f"TRIGGER NAME: {self.trigger}")
            # print(f"NAMES: {self.names}")
            index = self.names.index(self.trigger)
            self.trigger = self.names[index + 1]
            # print(f"NEW TRIGGER: {self.trigger}")

    def setStep(self, name, step):
        """
        This function will set a condition to a certain step.
        Input "name" is the name of the condition to change.
        Input "step" is an integer for which step to set.
        Returns 0 for success, or 1 for failure.
        """
        # Look for the named condition
        for condition in self.names:
            if name == condition:
                self.currentStep = step
                return 0
        return 1

    def getNames(self):
        """
        Get all acceptable names of this condition
        """
        return self.names

    def getDescription(self):
        """
        Get current description based on this condition's state
        """
        return self.descriptions[self.currentStep]

    # TODO: The following function can be removed later, if desired.

    def printCondition(self):
        """
        Prints condition status for debugging purposes
        """
        print(f"\nCondition names: {self.names}")
        print(f"Current trigger: {self.trigger}")
        print(f"Looping? {self.loop}")
        print("Descriptions:")
        for i in range(self.totalSteps):
            print(f"Step {str(i)}: {self.descriptions[i]}")
