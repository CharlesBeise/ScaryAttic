__all__ = ['examine', 'take', 'inventory', 'drop', 'hide', 'help',
           'listen', 'peel', 'use', 'go', 'openVerb', 'look', 'eat',
           'savegame', 'loadgame', 'close', 'shake', 'flip']


"""
All functions take one parameter "info", which is a dict object containing the
folowing:
{
    "Player": Player object,
    "Game": Game object,
    "Verb": A list of verbs detected in the input,
    "Items": A list of items/features that the user can interact with,
    "Combination": True/False based on if a combination word was detected
                    (and, on, with),
    "Rooms": A list of Room name or directional words detected in input
}
"""

# Generic message to be used when input cannot be processed successfully
errorString = "I'm not sure what you mean. Try something else."


def examine(info):
    """
    Action function prints Item or Room feature details (specified by
    verbInteractions attribute).
    """
    # No item requested
    if len(info["Items"]) == 0:
        print(errorString)
        return

    # Get target name that the player wants to examine from input
    examineTarget = info["Items"][0]

    if examineTarget == "polaroid":
        examineTarget = identifyPolaroid(info["Player"])

    # Gather list of accessible items
    inventoryList = info["Player"].getInventory()
    roomItemList = info["Player"].getLocation().getAccessibleItems()
    allItems = inventoryList + roomItemList

    # Look for item with target name in player inventory and current room
    for item in allItems:
        if examineTarget == item.getName():
            # Get examine verb interaction for item
            result = item.verbResponses("Examine")
            if result == "None":  # This should not occur for defined Items
                print("There is no information about this item.")
            else:
                print(result)
            return

    # Look for Examine verb and target in current room verb interactions
    print(info["Player"].getLocation().verbResponses("Examine", examineTarget))


def identifyPolaroid(player):
    """
    This is a helper function used to identify which polaroid the player is
    referring to
    """
    items = player.getInventory() + player.getLocation().getAccessibleItems()
    options = []
    for item in items:
        if item.getName()[:-1] == "polaroid":
            options.append(item.getName())
    if len(options) == 0:
        return None
    elif len(options) == 1:
        return options[0]
    response = "Which one are you referring to: "
    for option in options:
        response = response + option + ', '
    selection = input(response[:-2] + '?\n')
    if (selection == "polaroid1" or "1") and "polaroid1" in options:
        return "polaroid1"
    elif (selection == "polaroid2" or "2") and "polaroid2" in options:
        return "polaroid2"
    elif (selection == "polaroid3" or "3") and "polaroid3" in options:
        return "polaroid3"
    else:
        return None


def take(info):
    """
    This function removes an item from the player's current room and adds it to
    their inventory
    """
    # No object requested
    if len(info["Items"]) == 0:
        print(errorString)
        return

    game = info["Game"]
    item = info["Items"][0]
    player = game.getPlayer()
    room = player.getLocation()

    # Make sure player can only take items that are accessible
    if item == "polaroid":
        result = None
        options = ["polaroid1", "polaroid2", "polaroid3"]
        for i in range(len(options)):
            result = room.removeAccessibleItem(options[i])
            room.triggerCondition(item)
            if result:
                item = options[i]
                break
    else:
        result = room.removeAccessibleItem(item)
        room.triggerCondition(item)

    if result:
        player.addInventory(result)
        for possession in player.getInventory():
            if possession == item:
                print(possession.verbResponses("Take"))
                return
    else:
        print(errorString)


def drop(info):
    """
    This function removes an item from the player's inventory and leaves it in
    the player's current room.
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    game = info["Game"]
    player = game.getPlayer()
    room = player.getLocation()
    for item in info["Items"]:
        if item == "polaroid":
            item = identifyPolaroid(player)
            if item is None:
                print("You don't have that.")
                return
        for possession in player.getInventory():
            if possession == item:
                print(possession.verbResponses("Drop"))
                player.removeInventory(item)
                room.addDroppedItem(possession)
                continue


def verbHelper(item, player, room, option):
    """
    This is a helper function for openVerb(), it handles the scenario where the
    item the user is trying to interact with is an Item object
    """
    if item == "polaroid":
        item = identifyPolaroid(player)
    for possession in player.getInventory():
        if possession == item:
            if possession.verbResponses(option) != "None":
                print(possession.verbResponses(option))
            else:
                print(errorString)
            return True
    if item in room.getAccessibleItems():
        print("You have to pick it up first.")
        return True
    return False


def openVerb(info):
    """
    This function allows a player to open an item or feature
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Open"):
        return
    print(room.verbResponses("Open", item))


def close(info):
    """
    This function allows a player to close an item or feature
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Close"):
        return
    print(room.verbResponses("Close", item))


def shake(info):
    """
    This function allows a player to shake an item or feature
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Shake"):
        return
    print(room.verbResponses("Shake", item))


def flip(info):
    """
    This function allows a player to flip over an item or feature
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Flip"):
        return
    print(room.verbResponses("Flip", item))


def help(info):
    response = "\n============= HELP =============\n" \
               "To play the game, enter a command.\n" \
               "Below is a list of verbs the game will accept.\n" \
               "Combine these verbs with objects in order to progress.\n" \
               "This is not an exhaustive list, so if you're stuck,\n" \
               "try something different and keep exploring!\n\n"

    help = "Help: Show this menu again."
    inventory = "Inventory: Show the items you currently hold."
    save = "Savegame: Save your current progress."
    load = "Loadgame: Load an existing game file."
    look = "Look: Display an extended description of the current room."
    lookat = "Look at: Describe an object."
    go = "Go: Switch rooms through a described exit."
    take = "Take: Pick up an item."
    drop = "Drop: Leave an item in the current room."
    use = "Use: Use an object somewhere or with something."

    keywords = [
        help,
        inventory,
        save,
        load,
        look,
        lookat,
        go,
        take,
        drop,
        use
    ]

    for word in keywords:
        response = response + "- " + word + '\n'

    print(response[:-1])


def inventory(info):
    header = "\nCurrent inventory: \n" \
             "-------------------\n"
    content = ""
    for item in info["Player"].getInventory():
        content = content + "- " + item.getName() + "\n"

    if content != "":
        print(header + content[:-1])
    else:
        print(header + "Empty")


def hide(info):
    """
    Action function allows the player to hide somewhere.
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Hide"):
        return
    print(room.verbResponses("Hide", item))


def peel(info):
    """
    Action function allows the player to peel/pull something.
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Peel"):
        return
    print(room.verbResponses("Peel", item))


def listen(info):
    """
    Action function allows the player to listen to something.
    """
    if len(info["Items"]) == 0:
        print(errorString)
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if verbHelper(item, player, room, "Listen"):
        return
    print(room.verbResponses("Listen", item))


def use(info):
    print("Using...")


def goStairsHelper(roomTarget, currentRoomName):
    """
    Helper function returns the destination room name when the player
    only specifies a form of stairs as a destination. If the current
    room has no stairs, then returns None.
    """
    stairsDict = {
        "upperHall": {"upstairs": None, "downstairs": "lowerHall"},
        "lowerHall": {"upstairs": "upperHall", "downstairs": "basement"},
        "basement": {"upstairs": "lowerHall", "downstairs": None}
    }
    # Confirm this room has stairs
    if currentRoomName not in stairsDict.keys():
        return None
    # If stairs in this room go up, return room name above
    if roomTarget in ["upstairs", "up"] and stairsDict[currentRoomName]["upstairs"] is not None:
        return stairsDict[currentRoomName]["upstairs"]
    # If stairs in this room go down, return room name below
    if roomTarget in ["downstairs", "down"] and stairsDict[currentRoomName]["downstairs"] is not None:
        return stairsDict[currentRoomName]["downstairs"]
    # Determine upstairs or downstairs if not specified
    if roomTarget not in ["stairs", "staircase"]:
        return None
    if stairsDict[currentRoomName]["upstairs"] is not None:
        if stairsDict[currentRoomName]["downstairs"] is not None:
            # If more than one stairs in this room, prompt for which stairs
            stairsInput = input("Which stairs? Up or down?\n")
            if stairsInput in ["up", "upstairs"]:
                return stairsDict[currentRoomName]["upstairs"]
            elif stairsInput in ["down", "downstairs"]:
                return stairsDict[currentRoomName]["downstairs"]
            else:
                return None
        # If only upstairs, return room name upstairs
        else:
            return stairsDict[currentRoomName]["upstairs"]
    # If only downstairs, return room name downstairs
    elif stairsDict[currentRoomName]["downstairs"] is not None:
        return stairsDict[currentRoomName]["downstairs"]
    return None


def goLockedHelper(destination, currentRoom):
    """
    Helper function prints the appropriate response to the player
    attempting to enter a locked room. Response depends on destination.
    """
    lockedResponse = {
        "attic": "The attic door is too high to reach.",
        "lowerHall": "It's too dark to go down the stairs safely.",
        "basement": "There is a combination lock on the basement door."
    }
    if destination in lockedResponse.keys():
        print(lockedResponse[destination])
    else:
        print("That room is locked.")


def goRoomHelper(roomInfo, currentRoom):
    """
    Helper function returns a destination from room info list that
    has been parsed from user input. If destination is invalid, then
    returns None.
    """
    if len(roomInfo) == 0 or len(roomInfo) > 2:
        return None
    if roomInfo[0] in ["stairs", "staircase", "upstairs", "downstairs", "up", "down"]:
        return goStairsHelper(roomInfo[0], currentRoom.getName())
    # Match name of connected Room to input room info
    for roomName, direction in currentRoom.getAllExits().items():
        if roomInfo[0] == roomName.lower() or roomInfo[0] == direction:
            return roomName
    currentRoomName = currentRoom.getName().lower()
    if roomInfo[0] == currentRoomName:
        return currentRoom.getName()
    if len(roomInfo) == 2 and roomInfo[1] == currentRoomName:
        return currentRoom.getName()
    return None


def go(info):
    """
    Action function moves player from one room to another. Takes info
    object as parameter and evaluates if specified movement is possible.
    If possible, moves Player and updates state.
    """
    # Find current Room and name of destination Room
    currentRoom = info["Player"].getLocation()
    destination = goRoomHelper(info["Rooms"], currentRoom)
    if destination is None:  # Invalid destination
        print(errorString)
        return
    if currentRoom.getName() == destination:
        print("You are already in that room.")
        return
    # Update Player location to valid destination Room
    for room in info["Game"].getRooms():
        if room.getName() == destination:
            if room.isLocked():
                goLockedHelper(destination, currentRoom)
                return
            info["Player"].setLocation(room)
            if room.isVisited():
                print(room.getShortDescription())
            else:
                print(room.getLongDescription())
                room.setVisited()


def look(info):
    """
    Action function prints the long description of the Player's current room.
    """
    print(info["Player"].getLocation().getLongDescription())


def eat(info):
    """
    Action function prints response to the Player attempting to eat various
    Items or Room features.
    """
    if len(info["Items"]) == 0:
        print("You're thinking about eating something, but what?")
        return
    # Get target name that the player wants to eat from input
    eatTarget = info["Items"][0]
    # Look for item with target name in player inventory and current room
    inventoryList = info["Player"].getInventory()
    roomItemList = info["Player"].getLocation().getAccessibleItems()
    allItems = inventoryList + roomItemList
    if eatTarget == "polaroid":
        eatTarget = identifyPolaroid(info["Player"])
    for item in allItems:
        if eatTarget == item.getName():
            # Get eat verb interaction for item
            result = item.verbResponses("Eat")
            if result == "None":
                print("You can't eat that.")
            else:
                print(result)
            return
    # Look for Eat verb and target in current room verb interactions
    print(info["Player"].getLocation().verbResponses("Eat", eatTarget))


def savegame(info):
    """
    Action function allows the player to save the current state of
    the Game.
    """
    info["Game"].saveGame()


def loadgame(info):
    """
    Action function allows the player to load and play a previously
    saved game state.
    """
    info["Game"].loadGame()
