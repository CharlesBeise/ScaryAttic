import re
from actionVerbs import *


verbDict = {"look": ["look"],
            "examine": ["lookat", "examine", "inspect"],
            "go": ["go", "exit"],
            "take": ["take", "grab", "pickup"],
            "help": ["help"],
            "inventory": ["inventory"],
            "savegame": ["savegame"],
            "loadgame": ["loadgame"],
            "open": ["open"],
            "close": ["close", "shut"],
            "hide": ["hide"],
            "listen": ["listen"],
            "peel": ["peel", "pull"],
            "use": ["use"],
            "drop": ["drop", "leave"],
            "eat": ["eat"],
            "shake": ["shake", "ring"],
            "flip": ["flip"]}

compoundWords = {"pick": "up",
                 "tin": "can",
                 "can": "opener",
                 "polaroid": "photo",
                 "silver": "bell",
                 "look": "at"}

itemList = ["ladder", "flashlight", "battery", "key", "canopener", "tincan",
            "bell", "polaroidphoto"]

combinationWords = ["with", "and", "on"]


def parse(userText):
    # Remove punctuation symbols and break command into individual words
    command, n = re.subn('[!?.,]', "", userText)
    tokens = command.lower().split()

    # Conduct an initial parse of the user input to identify compound words
    # (e.g., "pick up, look at, tin can")
    for i in range(len(tokens)):
        for key, value in compoundWords.items():
            if tokens[i] == value:
                if (i > 0) and (tokens[i - 1] == key):
                    tokens[i - 1] = key + value
                    tokens[i] = ""

    # Conduct a second parse to identify the relevant words in the user command
    modifiedCommand = []
    for token in tokens:
        for key, value in verbDict.items():
            if token in value:
                modifiedCommand.append(key)
        if token in itemList:
            modifiedCommand.append(token)
        elif token in combinationWords:
            modifiedCommand.append(token)

    print(modifiedCommand)

    """
    USAGE: globals()function(parameters)
    
    EXAMPLE:
    
    def greeting(name):
        print("Hello " + name)
        
    func = "greeting"
        
    globals()func(Susan)
    
    Output: "Hello Susan"
    """
    globals()[modifiedCommand[0]](modifiedCommand[1])


if __name__ == "__main__":
    userCommand = input("> ")
    parse(userCommand)

"""
Current issues with the parser:

- May be difficult to differentiate between when a user is talking about the 
"polaroid photo" or a random photo hanging on the wall. 
POSSIBLE SOLUTION: Only use the word "photo" to describe the polaroid photo. 
For anything else, use painting, portrait, or drawing

- NOTE: I think we should use the term "examine" instead of "look at", this
will help differentiate between "look" and "look at".
"""