from Classes.player import Player
from Classes.room import Room


__all__ = ['examine', 'take']


def examine(item):
    print("That is an interesting", item)


def take(item):
    print("You have added the " + item + " to your inventory")

def go(player: Player, destination: str, roomList: list):
    """
    Action moves player from one room to another. Takes Player and Room
    objects as parameters and evaluates if specified movement is possible.
    If possible, moves player and updates state.
    """
    currentRoom = player.getLocation().replace(" ", "").lower()
    destination = destination.replace(" ", "").lower()
    if currentRoom == destination:
        print("You are already in that room.")
    for room in roomList:
        if room.getName().replace(" ", "").lower() == currentRoom:
            # Get available exits from current room
            available = room.getAllExits()
            destinationRoom = room
    if available:
        for key, value in available.items():
            # Determine if destination is available exit and update player
            if key.replace(" ", "").lower() == destination or value.replace(" ", "").lower() == destination:
                player.setLocation(key)
                print(destinationRoom.getLongDescription())
                return
    print("That is not somewhere you can go from your current location.")    
