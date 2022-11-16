class Conditional:
    """
    Conditionals are used in Rooms, as anything that may change status.
    It takes the "conditions" JSON data from the
    Room where it is located.

    Input "name" as String for this condition.
    Input "loop" expects a string reading "True" or "False".
    Input "type" designates whether this condition applies to the room
       description or a feature description.
    Input "descriptions" takes a list of descriptions per step.
    """
    def __init__(self, name, seq, verbs, loop, type, descriptions):
        # The name of the condition
        self.name = name

        # List containing full trigger sequence
        self.seq = seq
        self.verbs = verbs

        # Attribute "trigger" is the current name of this condition,
        # which is required to proceed to the next step.
        self.trigger = self.seq[0]
        self.triggerVerbs = self.verbs[0]

        # Loop attribute determines if this is a condition that can
        # toggle back and forth (True) or if it only progresses forward (False)
        if loop.lower() == "true" or loop is True:
            self.loop = True
        else:
            self.loop = False

        # Type attribute is expected to be either "room" or "feature"
        self.type = type.lower()

        # Initialize current state of the condition
        self.currentStep = 0

        # Get total number of steps for this condition
        self.totalSteps = len(descriptions)

        # A list of all descriptions for this item's various states
        self.descriptions = descriptions

    def __eq__(self, other):
        """
        This method allows the Condition instance to its name
        when compared to a String.
        """
        if isinstance(other, str):
            if other.lower() == self.name:
                return True
        else:
            return False

    def triggerCondition(self, trigger):
        """
        Increments current state by one step.
        Use this to move the condition's progress forward.
        """
        # If needed, increment to the next trigger
        result = self.nextTrigger()

        # print(f"Incrementing to condition: {self.trigger}")

        # If this condition loops, it will go back around to step 0 at the
        # end of its steps
        if self.loop and self.currentStep >= (self.totalSteps - 1):
            self.currentStep = 0
        elif self.loop:
            self.currentStep += 1
        # If this condition has not reached its final step yet
        elif not self.loop and self.currentStep < (self.totalSteps - 1):
            self.currentStep += 1

        return result

    def nextTrigger(self):
        """
        This function increments the trigger word for the condition.
        """
        # If there are more triggers in line, set the next trigger
        index = self.seq.index(self.trigger)
        if index != len(self.seq) - 1:
            self.trigger = self.seq[index + 1]
            self.triggerVerbs = self.verbs[index + 1]
            return True
        else:
            return False

    def setStep(self, name, step):
        """
        This function will set a condition to a certain step.
        Input "name" is the name of the condition to change.
        Input "step" is an integer for which step to set.
        Returns 0 for success, or None for failure.
        """
        # Look for the named condition
        for condition in self.seq:
            if name == condition:
                self.currentStep = step
                return 0
        return None

    def getNames(self):
        """
        Get all acceptable names of this condition
        """
        return self.seq

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
        print(f"\nCondition name: {self.name}")
        print(f"Trigger sequence: {self.trigger}")
        print(f"Current trigger: {self.trigger}")
        print(f"Type of condition: {self.type}")
        print(f"Looping? {self.loop}")
        print("Descriptions:")
        for i in range(self.totalSteps):
            print(f"Step {str(i)}: {self.descriptions[i]}")
