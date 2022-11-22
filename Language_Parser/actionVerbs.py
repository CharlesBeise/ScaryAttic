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

    game = info["Game"]
    player = game.getPlayer()
    room = player.getLocation()
    allItems = player.getInventory() + room.getAccessibleItems()

    # Get target name that the player wants to examine from input
    examineTarget = info["Items"][0]

    examineTarget = polaroidHelper(player, examineTarget, allItems)

    try:
        if "flashlight" in examineTarget:
            examineTarget = getSteppedItemName(allItems, examineTarget)
    except TypeError:
        pass

    # Look for item with target name in player inventory and current room
    for item in allItems:
        if examineTarget == item.getName():
            # Get examine verb interaction for item
            result = item.getDescription()
            if result == "None":  # This should not occur for defined Items
                print("There is no information about this item.")
            else:
                # Print both image and description
                printItemImage(item, "front")
                print(textwrap.fill(result, fillWidth))
            return

    # Look for Examine verb and target in current room verb interactions
    response = info["Player"].getLocation().verbResponses(
        "Examine", examineTarget)
    print(textwrap.fill(response, fillWidth))


def printItemImage(item, imageName):
    """
    Attempts to print an item's image, if it exists.
    Input 'item' is an Item object, 'imageName' is the image being requested.
    Returns True is successful or False if it fails.
    """
    if item.images:
        try:
            print(item.images[imageName])
            return True
        except (KeyError, ValueError, AttributeError, IndexError):
            pass
    return False


def identifyPolaroid(player):
    """
    This is a helper function used to identify which polaroid the player is
    referring to
    """
    items = player.getInventory() + player.getLocation().getAccessibleItems()
    options = []
    for item in items:
        if item.getName()[:-1] == "polaroid":
            options.append(item.getInventoryName())
    if len(options) == 0:
        return None
    elif len(options) == 1:
        return options[0]
    response = "Which one are you referring to: "
    for option in options:
        response = response + option + ', '
    selection = input(response[:-2] + '?\n').lower().replace(" ", "")
    if selection == "polaroid" and "Polaroid" in options:
        return "polaroid1"
    elif (selection == "oldpolaroid" or selection == "old") and "Old Polaroid" in options:
        return "polaroid2"
    elif (selection == "dustypolaroid" or selection == "dusty") and "Dusty Polaroid" in \
            options:
        return "polaroid3"
    else:
        return None


def getFloorLocation(currentRoom):
    """
    Helper function takes player's current room and the game data.
    Returns "upstairs" or "downstairs" string based on which floor
    of the house the player is currently located in.
    """
    upstairs = ["masterBedroom", "bathroom", "secondBedroom",
                "upperHall", "utilityRoom", "attic"]
    if currentRoom in upstairs:
        return "upstairs"
    else:
        return "downstairs"


def polaroidHelper(player, itemName, itemList):
    """
    Helper function checks if this item is a polaroid, and if so,
    if it's the only polaroid in the given item list or not.
    """
    foundItem = itemName

    if itemName in ["polaroid2", "polaroid3"] or "polaroid" not in itemName:
        return itemName

    # Check if there is more than one polaroid in the list
    polaroidsCount = 0
    for i in itemList:
        if "polaroid" in i.name:
            polaroidsCount += 1

    # If there's more than one in the list, prompt the player to specify
    if "polaroid" in itemName and polaroidsCount > 1:
        foundItem = identifyPolaroid(player)
    # Otherwise, just return the only polaroid available
    else:
        for i in itemList:
            if itemName in i.name:
                foundItem = i.name
                break
    return foundItem


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

    # Check item name
    item = polaroidHelper(player, item, room.getAccessibleItems())
    if "flashlight" in item:
        allItems = player.getInventory() + room.getAccessibleItems()
        item = getSteppedItemName(allItems, item)

    # Counts number of Polaroids player has collected
    if "polaroid" in item and item in room.getVisibleItems():
        player.incPolaroids()

    # Remove item
    result = room.removeAccessibleItem(item)

    if result:
        room.triggerConditionRoom(result, "Take")
        player.addInventory(result)
        print(result.verbInteractions["Take"])

        # If player is picking up the working flashlight...
        if item == "flashlight3":
            if getFloorLocation(room) == "upstairs":
                game.unlockRoomByName("lowerHall")
                triggerOtherRoomCondition(
                    "upperHall", game, "flashlight", "Take")
            else:
                game.unlockRoomByName("upperHall")
                triggerOtherRoomCondition(
                    "lowerHall", game, "flashlight", "Take")
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
    item = info["Items"][0]
    allItems = player.getInventory() + room.getAccessibleItems()

    # Remove item from the room
    item = polaroidHelper(player, item, player.getInventory())
    if "flashlight" in item:
        item = getSteppedItemName(allItems, item)
    for possession in player.getInventory():
        if possession.name == item:
            print(possession.verbResponses("Drop"))
            player.removeInventory(item)
            room.addDroppedItem(possession)

            # If player is dropping the working flashlight...
            if possession == "flashlight3":
                if getFloorLocation(room) == "upstairs":
                    game.lockRoomByName("lowerHall")
                    triggerOtherRoomCondition(
                        "upperHall", game, "flashlight", "Drop")
                else:
                    game.lockRoomByName("upperHall")
                    triggerOtherRoomCondition(
                        "lowerHall", game, "flashlight", "Drop")
            return

    # If it couldn't be picked up
    if item in room.getVisibleItems():
        print("You have to pick it up first.")
    else:
        print(errorString)


def verbHelper(item, player, room, verb):
    """
    This is a helper function for openVerb(), it handles the scenario where the
    item the user is trying to interact with is an Item object
    """
    allItems = player.getInventory() + room.getAccessibleItems()
    item = polaroidHelper(player, item, allItems)
    for possession in player.getInventory():
        if possession == item:
            if possession.verbResponses(verb) != "None":
                if verb == "Flip" and "polaroid" in item:
                    printItemImage(possession, "back")
                print(possession.verbResponses(verb))
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
    combo = info["Combination"]

    if len(info["Items"]) == 2 and combo:
        try:
            if {"canOpener", "tinCan"} == {info["Items"][0], info["Items"][1]}:
                use(info)
            return
        except IndexError:
            pass

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
    game = info["Game"]
    item = info["Items"][0]
    room = player.getLocation()

    # Case for game win condition
    if room == "porch" and item == "silverBell":
        print("You jingle the silver bell. "
              "There's a sudden, violent rustle from the bushes.")
        if game.foodInDish:
            game.triggerBellCondition()
        return

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
    """
    Calls the game's help menu.
    """
    info["Game"].printHelp()


def inventory(info):
    header = "\nCurrent inventory: \n" \
             "-------------------\n"
    content = ""
    for item in info["Player"].getInventory():
        content = content + "- " + item.getInventoryName() + "\n"

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


def combineItemAndFeature(player, game, item, feature):
    """
    Helper function for 'useHandler'.
    Takes player, game, and two strings of the item and feature names.
    Returns None if the combination fails.
    """
    atticValues = {"attic", "hatch", "ceiling", "up", "upstairs"}
    # Since order of words doesn't matter, choose an order for processing
    if "ladder" in (item, feature) and \
            (item in atticValues or feature in atticValues):
        item = "ladder"
        feature = "hatch"
        itemData = getItemDataForUse(player, item)
    elif {item, feature} == {"key", "chest"}:
        item = "key"
        feature = "chest"
        itemData = getItemDataForUse(player, item)
    elif {item, feature} == {"catFood", "dish"}:
        item = "catFood"
        feature = "dish"
        itemData = getItemDataForUse(player, item)
    else:
        itemData = []

    currentRoom = player.getLocation()

    # Look up the item's verb interaction response, if there is one
    try:
        response = itemData["object"].getVerbInteraction("Use")
    except (KeyError, ValueError, IndexError, TypeError):
        response = None

    if response != "None":
        # Case for "ladder", "hatch"
        if {item, feature} == {"ladder", "hatch"}:
            # Remove ladder from inventory
            removeOldItem(player, itemData["object"], itemData["location"])
            # Trigger any room conditions
            currentRoom.triggerConditionRoom(item, "Use")
            # Unlock attic
            game.unlockRoomByName("attic")
        elif {item, feature} == {"key", "chest"}:
            # Remove key from inventory
            removeOldItem(player, itemData["object"], itemData["location"])
            # Trigger any room conditions (unlock chest)
            currentRoom.triggerConditionRoom(item, "Use")
        elif {item, feature} == {"catFood", "dish"}:
            # Remove cat food from inventory
            removeOldItem(player, itemData["object"], itemData["location"])
            # Trigger any room conditions (unlock chest)
            currentRoom.triggerConditionRoom(item, "Use")
            # Trigger game win condition
            game.triggerFoodCondition()
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


def triggerOtherRoomCondition(roomName, game, condName, condVerb):
    """
    Helper function will trigger a condition in a specified room
    (Useful for cases outside the player's current location.)
    """
    for room in game.rooms:
        if room == roomName:
            room.triggerConditionRoom(condName, condVerb)


def batteryFlashlight(player, game, itemData1, itemData2):
    """
    Helper function for 'combineTwoItems' -
    applies a battery item to the flashlight item.
    """
    numFlashlights = 3

    # Battery and previous flashlight are removed & consumed
    removeOldItem(player, itemData1["object"], itemData1["location"])
    triggerOtherRoomCondition("upperHall", game, "flashlight", "Use")
    player.getLocation().triggerConditionRoom(itemData1["name"], "Use")

    # Remove existing flashlight from its location
    removeOldItem(player, itemData2["object"], itemData2["location"])

    # If the flashlight is still upgradable, get the upgrade name
    if itemData2["index"] < numFlashlights:
        upgradeIndex = str(itemData2["index"] + 1)
        upgradeName = "flashlight" + upgradeIndex

        # Place the upgrade back where the old one was
        upgrade = game.removeFromItemStorage(upgradeName)
        placeNewItem(player, upgrade, itemData2["location"])
        game.removeFromItemStorage(upgrade.name)

        # If this is the last (working) flashlight, unlock the stairs and
        # light up the upperHall
        if upgradeName == "flashlight3":
            game.unlockRoomByName("lowerHall")
            triggerOtherRoomCondition("upperHall", game, "flashlight", "Use")


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
    elif {"canOpener", "tinCan"} == {item1, item2}:
        item1 = "canOpener"
        item2 = "tinCan"
        itemData1 = getItemDataForUse(player, item1)
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
    except (KeyError, ValueError, IndexError, TypeError):
        return None

    # Handle valid cases here
    if "battery" in (item1, item2):
        batteryFlashlight(player, game, itemData1, itemData2)
    elif {item1, item2} == {"canOpener", "tinCan"}:
        if itemData2["location"] != "inv":
            return "You have to pick it up first."
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
        response = combineItemAndFeature(player, game, item1, item2)
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
    itemExists = False

    # Locate item object
    for item in inv:
        if itemName in item.name:
            itemUseData["object"] = item
            itemUseData["location"] = "inv"
            itemExists = True
            break
    for item in roomVis:
        if itemName in item.name:
            itemUseData["object"] = item
            itemUseData["location"] = "roomVis"
            itemExists = True
            break
    for item in roomDrop:
        if itemName in item.name:
            itemUseData["object"] = item
            itemUseData["location"] = "roomDrop"
            itemExists = True
            break

    if itemExists:
        # Get step index for the current item (count starts with 1)
        digits = [int(i) for i in itemUseData["object"].name if i.isdigit()]
        try:
            itemIndex = int("".join(str(i) for i in digits))
            itemUseData["index"] = itemIndex
        # Sets step to 1 if it doesn't exist
        except ValueError:
            itemUseData["index"] = 1
    else:
        return None

    return itemUseData


def useSingleItem(player, currentRoom, item):
    """
    Helper function for 'use' processes the use of just one target item.
    Returns a string response back to 'use', or None if it fails.
    """
    allItems = player.getInventory() + currentRoom.getAccessibleItems()
    # This is a list of items that are restricted because they're used
    # on room features. Alternate 'use' descriptions are provided.
    featureItems = ["key", "catFood", "ladder"]
    if isItem(item, allItems):
        if item not in featureItems:
            if verbHelper(item, player, currentRoom, "Use"):
                return ""
            return currentRoom.verbResponses("Use", item, False)
        if item == "key":
            return "It could unlock something, but what?"
        elif item == "catFood":
            return "You could maybe use it if you were hungry."
        elif item == "ladder":
            return "It's good for reaching high places."
    else:
        return None


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

    # Handles "use" on one item (if item2 doesn't exist)
    if len(info["Items"]) == 1:
        item = info["Items"][0]
        item = polaroidHelper(player, item, allItems)
        response = useSingleItem(player, currentRoom, item)
        if response == "":
            return
    elif len(info["Items"]) == 2 and combo:
        item1 = info["Items"][0]
        item2 = info["Items"][1]
        item1 = polaroidHelper(player, item1, allItems)
        item2 = polaroidHelper(player, item2, allItems)
        response = useHandler(player, game, allItems, item1, item2)
    else:
        response = errorString

    if response is None:
        response = "That won't work."

    print(textwrap.fill(response, fillWidth))


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
    if roomTarget in ["upstairs", "up", "hatch", "ceiling"] \
            and stairsDict[currentRoomName]["upstairs"] is not None:
        return stairsDict[currentRoomName]["upstairs"]
    # If stairs in this room go down, return room name below
    if roomTarget in ["downstairs", "down"] \
            and stairsDict[currentRoomName]["downstairs"] is not None:
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


def unlockBasement(prompt, game):
    """
    Helper function allows the player to try a combination code
    to unlock the basement.
    """
    correctCode = "597"

    print(f"{prompt} ")
    selection = input(
        "Would you like to try entering a code? (Y/N) ").lower()
    if selection == "y":
        print("\nThere are spaces for three numbers. "
              "You can enter as many as you like.")
        code = 0
        while code != "cancel":
            code = input(
                "Enter 3-digit code or 'cancel' to go back: ")
            code = ''.join(e for e in code if e.alnum())
            if code == correctCode:
                print("\nYou hear the lock slide open. "
                      "The door is now unlocked."
                      "\nYou step back into the Lower Hall.")
                game.unlockRoomByName("basement")
                return
    else:
        return


def goLockedHelper(destination, player, game):
    """
    Helper function prints the appropriate response to the player
    attempting to enter a locked room. Response depends on destination.
    """
    lockedResponse = {
        "attic": "The attic door is too high to reach.",
        "lowerHall": "It's too dark to go down the stairs safely.",
        "upperHall": "It's too dark to go up the stairs safely.",
        "basement": "There is a combination lock on the basement door."
    }

    # Check if player has all polaroids to try a code on the basement
    if destination == "basement" and player.polaroidsCollected == 3:
        unlockBasement(lockedResponse[destination], game)
        return

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
    if roomInfo[0] in ["stairs", "staircase", "upstairs", "downstairs",
                       "up", "down", "hatch", "ceiling"]:
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
                goLockedHelper(destination, info["Player"], info["Game"])
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
    player = info["Player"]
    item = info["Items"][0]
    room = player.getLocation()

    if verbHelper(item, player, room, "Eat"):
        return
    print(room.verbResponses("Eat", item))


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
