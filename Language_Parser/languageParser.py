import re
import json
from actionVerbs import examine, take


f = open('verbDictionary.json')
verbDict = json.load(f)
verbList = list(verbDict.keys())

f = open('combinationWords.json')
combinationWords = json.load(f)

f = open('compoundWords.json')
compoundWords = json.load(f)

f = open('itemList.json')
itemList = json.load(f)


def placeHolder(decoy):
    """
    This is a temporary workaround for flake8 error F401. It doesn't like that
    I don't explicitly call the imported functions, so they are being called in
    this unused function
    """
    examine(decoy)
    take(decoy)


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
    parsedInput = {"Verb": "",
                   "Items": [],
                   "Combination": False}
    for token in tokens:
        if token in verbList:
            parsedInput["Verb"] = verbDict[token]
        elif token in itemList:
            parsedInput["Items"].append(token)
        elif token in combinationWords:
            parsedInput["Combination"] = True

    """
    USAGE: globals()function(parameters)
    EXAMPLE:
    def greeting(name):
        print("Hello " + name)
    func = "greeting"
    globals()func(Susan)
    Output: "Hello Susan"
    """
    if len(parsedInput["Items"]) == 1:
        globals()[parsedInput["Verb"]](parsedInput["Items"][0])
    elif len(parsedInput["Items"]) > 1:
        print("Combination action")


if __name__ == "__main__":
    while True:
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
