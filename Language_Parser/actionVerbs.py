__all__ = ['examine', 'take', 'inventory', 'drop', 'hide', 'help',
           'listen', 'peel', 'use', 'go', 'openVerb']


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
"""


def examine(info):
    pass


def identifyPolaroid(player):
    """
    This is a helper function used to identify which polaroid the player is
    referring to
    """
    items = player.getInventory()
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
    if selection == "polaroid1" and "polaroid1" in options:
        return "polaroid1"
    elif selection == "polaroid2" and "polaroid2" in options:
        return "polaroid2"
    elif selection == "polaroid3" and "polaroid3" in options:
        return "polaroid3"
    else:
        return None


def take(info):
    """
    This function removes an item from the player's current room and adds it to
    their inventory
    """
    if len(info["Items"]) == 0:
        print("I don't think that will work.")
        return
    game = info["Game"]
    item = info["Items"][0]
    player = game.getPlayer()
    room = player.getLocation()
    if item == "polaroid":
        result = None
        options = ["polaroid1", "polaroid2", "polaroid3"]
        for i in range(len(options)):
            result = room.removeItem(options[i])
            if result:
                item = options[i]
                break
    else:
        result = room.removeItem(item)
    if result:
        player.addInventory(result)
        for possession in player.getInventory():
            if possession == item:
                print(possession.verbResponses("Take"))
                return
    else:
        print("You can't seem to find that item here.")


def drop(info):
    """
    This function removes an item from the player's inventory and leaves it in
    the player's current room.
    """
    if len(info["Items"]) == 0:
        print("I don't think that will work.")
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
                room.addItem(possession)
                continue


def openHelper(item, player, room):
    """
    This is a helper function for openVerb(), it handles the scenario where the
    item the user is trying to open is an Item object
    """
    for possession in player.getInventory():
        if possession == item:
            if possession.verbResponses("Open") != "None":
                print(possession.verbResponses("Open"))
            else:
                print("I don't think that will work.")
            return True
    if item in room.getItems():
        print("You have to pick it up first.")
        return True
    return False


def openVerb(info):
    """
    This function allows a player to open an item or feature
    """
    if len(info["Items"]) == 0:
        print("I don't think that will work.")
        return
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()
    if openHelper(item, player, room):
        return
    print(room.verbResponses("Open", item))


def close(info):
    """
    This function allows a player to close an item or feature
    """
    print("Close")


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

    print(response)


def inventory(info):
    header = "\nCurrent inventory: \n" \
             "-------------------\n"
    content = ""
    for item in info["Player"].getInventory():
        content = content + "- " + item.getName() + '\n'

    if content != "":
        print(header + content + "\n")
    else:
        print(header + "Empty" + "\n")


def hide(info):
    print("Hiding...")


def peel(info):
    print("Peeling...")


def listen(info):
    print("Listening...")


def use(info):
    print("Using...")


def goHelper(roomInfo, currentRoom):
    """
    Helper function returns a destination from room info list that
    has been parsed from user input. If destination is invalid, then
    returns None.
    """
    if len(roomInfo) == 0 or len(roomInfo) > 2:
        return None
    # Match name of connected Room to input room info
    for roomName, direction in currentRoom.getAllExits().items():
        if roomInfo[0] == roomName.lower() or roomInfo[0] == direction:
            return roomName
    currentRoomName = currentRoom.getName().lower()
    if roomInfo[0] == currentRoomName or roomInfo[1] == currentRoomName:
        return currentRoom.getName()
    return None


def go(info):
    """
    Action function moves player from one room to another. Takes info
    object as parameter and evaluates if specified movement is possible.
    If possible, moves Player and updates state.
    """
    # Find current Room and name of destionation Room
    currentRoom = info["Player"].getLocation()
    destination = goHelper(info["Rooms"], currentRoom)
    if destination is None:  # Invalid destination
        print("You can only go to one room connected to this room.")
    if currentRoom.getName() == destination:
        print("You are already in that room.")
    # Update Player location to valid destination Room
    for room in info["Game"].getRooms():
        if room.getName() == destination:
            info["Player"].setLocation(room)
            if room.isVisited():
                print(room.getShortDescription())
            else:
                print(room.getLongDescription())
                room.setVisited()
