__all__ = ['examine', 'take', 'inventory', 'drop']


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


def inventory(info):
    response = "You currently have the following items: "
    for item in info["Player"].getInventory():
        response = response + item.getName() + ','
    print(response[:-1])
