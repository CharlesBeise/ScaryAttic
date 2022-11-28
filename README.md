# ScaryAttic
Scary Attic is a text-based game that is played within a terminal window. The player must navigate their way through an old house, observing and interacting with various objects and their surroundings to uncover the source of strange sounds being heard at night. They will need to problem solve and be resourceful to make it to the end of the game.

## Installation Instructions
This game was written using Python 3, so it can be downloaded and played using a Python interpreter of your choice. We strongly reommend Python version 3.10 or later. The following commands will help to get started.

Clone repository to your local environment:

`git clone https://github.com/CharlesBeise/ScaryAttic.git`

Navigate to game directory:

`cd ScaryAttic`

Start game:

`python3 ./main.py`

## Game Instructions

1. Our game begins with a start-up menu. The player can enter “new” for a new game or “load” to load a saved game. 	You can enter “exit game” at any time to exit the game.

2. Once you’ve started or loaded a game, you will begin playing through the story of our game. There’s a mystery in the house that you will be trying to solve, based on the prompts.

3. You play the game by entering simple commands, such as: “Go north”, “Open the window”, or “Examine the bookshelf”. If you are stuck, you can view a list of allowed actions by entering the “Help” command. Players can also enter “inventory” to see which items they are currently holding.

   The game will respond to the player’s commands. If the game understands the command, it will perform the requested action. If not, the game will prompt the player to try something else.

   Commands are expected to be spelled correctly and ordered in the verb + noun format, but most commands can be written several different ways and still be understood. For example, capitalization does not matter, and many word synonyms are acceptable.

   The player should be able to examine everything in each room, and some items will also accept other forms of interaction.

   Room and item descriptions will sometimes change based on the player’s actions. For example, an item may be hidden the first time the player encounters it, but it may be revealed after an action is taken.

4. When the player has completed all necessary tasks in the game and solved the mystery, the conclusion to the story will be displayed. A complete walkthrough for the game has been provided below, but it does not include every interaction available within the game.

5. Here is a list and description of all the verb functions the player can use:

   | Verb | Description |
   | --- | --- |
   | `Help` | Show the help menu. |
   | `Inventory` | Show the items you currently hold. |
   | `Savegame` | Save your current progress. |
   | `Loadgame` | Load an existing game file. |
   | `Look` | Display an extended description of the room you are in. |
   | `Look at` | Display a description of the target of the command. |
   | `Go` | Switch rooms by direction or name. |
   | `Take` | Pick up an item. |
   | `Drop` | Leave an item in the current room. |
   | `Pull` | Pull or peel on an object. |
   | `Use` | Use something by itself or on something else. |
   | `Flip` | Flip an object. |
   | `Shake` | Shake an object. |
   | `Hide in` | Hide in something. |
   | `Listen` | Listen to something. |
   | `Eat` | Eat something. |
   | `Open` | Open something. |
   | `Close` | Close something. |
   | `Exit game` | Stop playing and close the game. |
