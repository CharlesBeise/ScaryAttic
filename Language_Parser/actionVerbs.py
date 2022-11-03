__all__ = ['examine', 'take', 'inventory', 'drop', 'hide', 'help',
           'listen', 'peel', 'use']


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
        for possession in player.getInventory():
            if possession == item:
                print(possession.verbResponses("Drop"))
                player.removeInventory(item)
                room.addItem(possession)
                continue


def openVerb(info):
    """
    This function allows a player to open an item or feature
    """
    print("Open")


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


def go(info):
    """
    Action function moves player from one room to another. Takes info
    object as parameter and evaluates if specified movement is possible.
    If possible, moves Player and updates state.
    """
    def goHelper(roomInfo, currentRoom):
        """
        Helper function returns a destination from room info list that
        has been parsed from user input. If destination is invalid, then
        returns None.
        """
        if len(roomInfo) == 0 or len(roomInfo) > 2:
            return None
        # Match name of connected Room to input room info
        for roomName, direction in currentRoom.getAllExits():
            if roomInfo[0] == roomName.lower() or roomInfo[0] == direction:
                return roomName
        currentRoomName = currentRoom.getName().lower()
        if roomInfo[0] == currentRoomName or roomInfo[1] == currentRoomName:
            return currentRoom.getName()
        return None

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
            print(room.getLongDescription())
