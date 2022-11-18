__all__ = ['examine', 'take', 'inventory', 'drop', 'hide', 'help',
           'listen', 'peel', 'use', 'go', 'openVerb', 'look', 'eat',
           'savegame', 'loadgame', 'close', 'shake', 'flip']
import textwrap


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

fillWidth = 75

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

    # Remove item from the room
    if "polaroid" in item:
        options = ["polaroid1", "polaroid2", "polaroid3"]
        for i in room.getAccessibleItems():
            if i in options:
                item = i.name
                break
    elif "flashlight" in item:
        allItems = player.getInventory() + room.getAccessibleItems()
        item = getSteppedItemName(allItems, item)

    result = room.removeAccessibleItem(item)

    if result:
        room.triggerConditionRoom(result, "Take")
        player.addInventory(result)
        print(result.verbInteractions["Take"])
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

    # Try to pick up the item
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
                return

    # If it couldn't be picked up
    if item in room.getAccessibleItems():
        print("You have to pick it up first.")
    else:
        print(errorString)


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
    if item in room.getVisibleItems():
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


def removeOldItem(player, item, location):
    """
    Helper function for 'use' and combining objects -
    removes an Item instance from the specified location.
    Location should be one of these strings: "inv", "roomVis", "roomDrop"
    """
    if location == "inv":
        player.removeInventory(item)
    elif location == "roomVis" or location == "roomDrop":
        player.getLocation().removeAccessibleItem(item)


def placeNewItem(player, item, location):
    """
    Helper function for 'use' and combining objects -
    places an instance of the Item in the specified location.
    Location should be one of these strings: "inv", "roomVis", "roomDrop"
    """
    if location == "inv":
        player.addInventory(item)
    elif location == "roomVis":
        player.getLocation().addVisibleItem(item)
    elif location == "roomDrop":
        player.getLocation().addVisibleItem(item)


def combineItemAndFeature(player, item, feature):
    """
    Helper function for 'useHandler'.
    Takes player, and two strings of the item and feature names.
    Returns None if the combination fails.
    """
    # Since order of words doesn't matter, choose an order for processing
    if {item, feature} == {"catFood", "dish"}:
        item = "catFood"
        feature = "dish"
        itemData = getItemDataForUse(player, item)
    else:
        itemData = []

    currentRoom = player.getLocation()

    # Look up item interaction response, if there is one
    try:
        response = currentRoom.verbResponses("Use", item, feature)
        # If that doesn't get a valid response, try swapping the inputs
        if response == "None":
            response = currentRoom.verbResponses("Use", feature, item)
    except (KeyError, ValueError, IndexError):
        response = None

    if response != "None":
        # Case for "catFood", "dish"
        if {item, feature} == {"catFood", "dish"} and currentRoom == "porch":
            # Remove catFood from inventory
            removeOldItem(player, itemData["object"], itemData["location"])
            # TODO: Call 'use' description

            # Trigger condition
            currentRoom.triggerCondition(feature, "Use")
        else:
            response = "That won't work."
        return response
    else:
        return None


def canOpenerCatFood(player, game, itemData2):
    """
    Helper function for 'combineTwoItems' -
    applies the can opener item to the tin can to get cat food.
    """
    # Remove & consume tinCan
    removeOldItem(player, itemData2["object"], itemData2["location"])

    # Replace the tinCan with the catFood from Game storage
    catFood = game.removeFromItemStorage("catFood")
    placeNewItem(player, catFood, itemData2["location"])


def batteryFlashlight(player, game, itemData1, itemData2):
    """
    Helper function for 'combineTwoItems' -
    applies a battery item to the flashlight item.
    """
    numFlashlights = 3

    # Battery and previous flashlight are removed & consumed
    removeOldItem(player, itemData1["object"], itemData1["location"])

    # Remove existing flashlight from its location
    removeOldItem(player, itemData2["object"], itemData2["location"])

    # If the flashlight is still upgradable, get the upgrade name
    if itemData2["index"] < numFlashlights:
        upgradeIndex = str(itemData2["index"] + 1)

        # Place the upgrade back where the old one was
        upgrade = game.removeFromItemStorage("flashlight" + upgradeIndex)
        placeNewItem(player, upgrade, itemData2["location"])
        game.removeFromItemStorage(upgrade.name)


def combineTwoItems(player, game, item1, item2):
    """
    Helper function for 'useHandler'.
    Takes player and game data, and two strings of item names.
    Returns None if the combination fails.
    The order of the item1 and item2 does not matter.
    """
    # Since order of words doesn't matter, choose an order for processing
    if "battery" in (item1, item2):
        if "flashlight" in item1:
            flashlight = item1
            item1 = item2
            item2 = flashlight
        itemData1 = getItemDataForUse(player, item1)
        itemData2 = getItemDataForUse(player, item2)
    elif {"canOpener", "tinCan"} in {item1, item2}:
        item1 = "canOpener"
        item2 = "tinCan"
        itemData1 = []  # canOpener doesn't need data
        itemData2 = getItemDataForUse(player, item2)
    else:
        return None

    # Look up item interaction response, if there is one
    try:
        response = \
            itemData2["object"].getItemInteraction(itemData1["name"])
        # If that doesn't get a valid response, try swapping the items
        if response == "None":
            response = \
                itemData1["object"].getItemInteraction(itemData2["name"])

    except (KeyError, ValueError, IndexError):
        return None

    # Handle valid cases here
    if "battery" in (item1, item2):
        batteryFlashlight(player, game, itemData1, itemData2)
    elif {item1, item2} == {"canOpener", "tinCan"}:
        canOpenerCatFood(player, game, itemData2)
    return response


def isItem(itemName, allItems):
    """
    Helper function for 'useHandler' - returns boolean based on whether the
    item is an "item" or a "feature".
    """
    for item in allItems:
        if itemName in item.name:
            return True
    return False


def getSteppedItemName(allItems, itemName):
    """
    Helper function takes the name of an item with multiple modes
    and returns the relevant one. Needs player data and a list of all
    items available to the player.
    If this item does not have an alternate name, return the original.
    """
    if "flashlight" in itemName:
        for item in allItems:
            if "flashlight" in item.name:
                return item.name
    return itemName


def useHandler(player, game, allItems, item1, item2):
    """
    Helper function for 'use' - reads the type of items and processes
    them depending on the type.
    Returns a response based on the case.
    """
    type1 = isItem(item1, allItems)
    type2 = isItem(item2, allItems)

    # Check if this is an item with multiple modes
    item1 = getSteppedItemName(allItems, item1)
    item2 = getSteppedItemName(allItems, item2)

    # Prevent using something on itself
    if item1 == item2:
        response = "You can't use an item on itself."
    # If one input is an Item, and the other a room feature
    elif {type1, type2} == {True, False}:
        response = combineItemAndFeature(player, item1, item2)
    # If both item1 and item2 are Items
    elif {type1, type2} == {True, True}:
        response = combineTwoItems(player, game, item1, item2)
    # Disallow using a feature on another feature
    elif {type1, type2} == {False, False}:
        response = "You can't use that."
    else:
        response = errorString

    return response


def getItemDataForUse(player, itemName):
    """
    Helper function for 'use' - gathers data about an item
    that the player is trying to use.
    Takes player and game data, and the item's name string.
    Returns a list with all the item's necessary data.
    """
    inv = player.getInventory()
    roomVis = player.getLocation().getVisibleItems()
    roomDrop = player.getLocation().getDroppedItems()

    # "itemUseData" dict will hold, in this order:
    # name (str): the item name provided by player
    # object (Item): the actual Item instance
    # location (str): "inv", "roomVis", or "roomDrop"
    # itemIndex (int): the current index of an item with multiple modes
    itemUseData = {"name": itemName}

    # Locate item object
    for item in inv:
        if itemName in item.name:
            itemUseData["object"] = item
            itemUseData["location"] = "inv"
            break
    for item in roomVis:
        if itemName in item.name:
            itemUseData["object"] = item
            itemUseData["location"] = "roomVis"
            break
    for item in roomDrop:
        if itemName in item.name:
            itemUseData["object"] = item
            itemUseData["location"] = "roomDrop"
            break

    # Get step index for the current item (count starts with 1)
    digits = [int(i) for i in itemUseData["object"].name if i.isdigit()]
    try:
        itemIndex = int("".join(str(i) for i in digits))
        itemUseData["index"] = itemIndex
    # Sets step to 1 if it doesn't exist
    except ValueError:
        itemUseData["index"] = 1

    return itemUseData


def use(info):
    """
    Action function allows the player to use an item or room feature.
    """
    # If no item is provided
    if len(info["Items"]) == 0:
        print(errorString)
        return

    player = info["Player"]
    game = info["Game"]
    combo = info["Combination"]
    currentRoom = player.getLocation()
    allItems = player.getInventory() + currentRoom.getAccessibleItems()

    # Identify the number of items provided
    try:
        item1 = info["Items"][0]
        item2 = info["Items"][1]
        numItems = 2
    except IndexError:
        item1 = info["Items"][0]
        item2 = None
        numItems = 1
    except (KeyError, ValueError):
        print("No items found")
        print(errorString)
        return

    # Handles "use" on one item (if item2 doesn't exist)
    if numItems == 1:
        print(currentRoom.verbResponses("Use", item1, False))
        return
    # Handles "use" on two items with a valid combination word
    elif numItems == 2 and combo:
        response = useHandler(player, game, allItems, item1, item2)

        if response is None:
            print("That won't work.")
        else:
            print(textwrap.fill(response, fillWidth))
    else:
        print(errorString)


def goStairsHelper(roomTarget, currentRoomName):
    """
    Helper function returns the destination room name when the player
    only specifies a form of stairs as a destination. If the current
    room has no stairs, then returns None.
    """
    stairsDict = {
        "attic": {"upstairs": None, "downstairs": "upperHall"},
        "upperHall": {"upstairs": "attic", "downstairs": "lowerHall"},
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


def goLockedHelper(destination):
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
        print("You can't go that way.")
        return
    if currentRoom.getName() == destination:
        print("You are already in that room.")
        return
    # Update Player location to valid destination Room
    for room in info["Game"].getRooms():
        if room.getName() == destination:
            if room.isLocked():
                goLockedHelper(destination)
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
