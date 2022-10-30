import re
import json
from actionVerbs import examine, take


verbDict = json.load(open('verbDictionary.json'))
verbList = list(verbDict.keys())

combinationWords = json.load(open('combinationWords.json'))

compoundWords = json.load(open('compoundWords.json'))

itemList = json.load(open('itemList.json'))


def placeHolder(decoy):
    """
    This is a temporary workaround for flake8 error F401. It doesn't like that
    I don't explicitly call the imported functions, so they are being called in
    this unused function
    """
    examine(decoy)
    take(decoy)


def findCompounds(phrase):
    """
    This function takes the tokenized user input and replaces any relevant
    compound words with a single word
    """
    # Conduct an initial parse of the user input to identify compound words
    # (e.g., "pick up, look at, tin can")
    for i in range(len(phrase)):
        for key, value in compoundWords.items():
            if phrase[i] == value:
                if (i > 0) and (phrase[i - 1] == key):
                    phrase[i - 1] = key + value
                    phrase[i] = ""

    return phrase


def siftInput(longText):
    """
    This function picks out the necessary words to complete the user's
    request
    """
    wordDict = {"Verb": "",
                "Items": [],
                "Combination": False}
    for token in longText:
        if token in verbList:
            wordDict["Verb"] = verbDict[token]
        elif token in itemList:
            wordDict["Items"].append(token)
        elif token in combinationWords:
            wordDict["Combination"] = True

    return wordDict


def parse(userText):
    # Remove punctuation symbols and break command into individual words
    command, n = re.subn('[!?.,]', "", userText)
    tokens = command.lower().split()

    tokens = findCompounds(tokens)

    # Conduct a second parse to identify the relevant words in the user command
    parsedInput = siftInput(tokens)

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
