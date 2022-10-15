import re

verbList = ["look", "look at", "inspect", "go", "exit", "take", "pick up",
            "help", "inventory", "savegame", "loadgame", "open", "close",
            "hide", "listen", "peel", "pull", "use", "drop", "leave", "eat",
            "shake", "ring", "flip"]

itemList = ["ladder", "flashlight", "battery", "key", "can opener", "tin can",
            "silver bell", "polaroid photo"]

combinationWords = ["with", "and", "on"]


def parse(userText):
    # Remove punctuation symbols and break command into individual words
    command, n = re.subn('[!?.,]', "", userText)
    tokens = command.split()
    print("Command: ", command)
    print("n: ", n)
    print("Tokens: ", tokens)


if __name__ == "__main__":
    userCommand = input("> ")
    parse(userCommand)

