from Classes.game import Game
# from Classes.player import Player
from Language_Parser.languageParser import parse


saveFile = "saveStates.json"


def gameStart(saveFile):
    # Initialize Game and load state
    game = Game(saveFile)
    game.titleScreen()
    game.selectGameState()
    player = game.getPlayer()
    # Begin user input loop to play game
    while game.isRunning():
        userInput = input("> ")
        parse(userInput, player, game)
        # if userInput.replace(" ", "").lower() == "exitgame":
        #     game.exitGame()
        # Parse user input for command/action


if __name__ == "__main__":

    gameStart(saveFile)
