import re
import json
from Language_Parser.actionVerbs import \
    examine, take, inventory, drop, help, hide, listen, peel, use, go, \
    openVerb, look, eat, savegame, loadgame, close, shake, flip  # noqa: F401
from Classes.player import Player
from Classes.game import Game


verbDict = json.load(open('Language_Parser/verbDictionary.json'))
verbList = list(verbDict.keys())

combinationWords = json.load(open('Language_Parser/combinationWords.json'))

compoundWords = json.load(open('Language_Parser/compoundWords.json'))

itemDict = json.load(open('Language_Parser/itemDictionary.json'))


def findCompounds(phrase):
    """
    This function takes the tokenized user input and replaces any relevant
    compound words with a single word
    """
    # Conduct an initial parse of the user input to identify compound words
    # (e.g., "pick up, look at, tin can")
    for i in range(len(phrase)):
        for key, value in compoundWords.items():
            if phrase[i] in value:
                if (i > 0) and (phrase[i - 1] == key):
                    phrase[i - 1] = key + phrase[i]
                    phrase[i] = ""

    return phrase


def siftInput(longText, player: Player, game: Game):
    """
    This function picks out the necessary words to complete the user's
    request
    """
    wordDict = {"Player": player,
                "Game": game,
                "Verb": [],
                "Items": [],
                "Combination": False,
                "Rooms": []}
    roomList = ["north", "south", "east", "west",
                "southwest", "southeast", "northwest", "northeast",
                "stairs", "staircase", "upstairs", "downstairs", "up", "down",
                "hatch", "ceiling"]
    for room in game.getRooms():
        roomList.append(room.getName().lower())
    for token in longText:
        for key, value in verbDict.items():
            if token in value:
                wordDict["Verb"].append(key)
                break
        for key, value in itemDict.items():
            if token in value:
                wordDict["Items"].append(key)
                break
        if token in combinationWords:
            wordDict["Combination"] = True
        if token in roomList:
            wordDict["Rooms"].append(token)

    return wordDict


def parse(userText, player, game):
    # Remove punctuation symbols and break command into individual words
    command, n = re.subn('[!?.,]', "", userText)
    tokens = command.lower().split()

    tokens = findCompounds(tokens)

    # Conduct a second parse to identify the relevant words in the user command
    parsedInput = siftInput(tokens, player, game)

    """
    USAGE: globals()function(parameters)
    EXAMPLE:
    def greeting(name):
        print("Hello " + name)
    func = "greeting"
    globals()func(Clarice)
    Output: "Hello Clarice"
    """
    if len(parsedInput["Verb"]) == 1:
        try:
            globals()[parsedInput["Verb"][0]](parsedInput)
        except KeyError:
            print("I'm sorry, I don't understand that command.")
    elif len(parsedInput["Verb"]) == 0 and len(parsedInput["Rooms"]) > 0:
        go(parsedInput)
    else:
        print("I'm sorry, I don't understand that command.")
