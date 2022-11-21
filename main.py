from Classes.game import Game
# from Classes.player import Player
from Language_Parser.languageParser import parse


def gameStart():
    # Initialize Game and load state
    game = Game()
    game.titleScreen()
    game.selectGameState()
    player = game.getPlayer()
    # Begin user input loop to play game
    while game.isRunning() and not game.checkForWin():
        userInput = input("\n> ")
        if userInput.replace(" ", "").lower() == "exitgame":
            game.exitGame()
        else:
            parse(userInput, player, game)
    if game.checkForWin():
        game.outro()
    else:
        print("\nThank you for playing Scary Attic.")
        print("We sincerely hope you enjoyed it.\n")


if __name__ == "__main__":

    gameStart()
