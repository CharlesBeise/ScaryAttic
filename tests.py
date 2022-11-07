import fnmatch
import os
import random
# import sys
import unittest
# from io import StringIO
from Classes.game import Game


# from Classes.player import Player
# import main


def randomSpaces(s):
    """
    This can be used to insert random spaces into a string.
    """
    s = list(s)
    for i in range(len(s) - 1):
        while random.randrange(2):
            s[i] = s[i] + " "
    return "".join(s)


def randomUppercase(s):
    """
    This can be used to capitalize letters of a string at random.
    """
    return ''.join(map(random.choice, zip(s.lower(), s.upper())))


def randomStr(s):
    """
    This can be used to insert BOTH random spaces and capitalization
    into a string.
    """
    return randomSpaces(randomUppercase(s))


class TestCase(unittest.TestCase):
    testGame = Game()
    directionList = [
        "north",
        "south",
        "east",
        "west",
        "northeast",
        "northwest",
        "southeast",
        "southwest"]

    ###################################################################
    #                                                                 #
    #                        Game tests                               #
    #                                                                 #
    ###################################################################

    def test_gamePlaceholder(self):
        pass

    ###################################################################
    #                                                                 #
    #                       Player tests                              #
    #                                                                 #
    ###################################################################

    def test_playerPlaceholder(self):
        pass

    ###################################################################
    #                                                                 #
    #                       Parser tests                              #
    #                                                                 #
    ###################################################################

    def test_parserPlaceholder(self):
        pass

    ###################################################################
    #                                                                 #
    #                        Item tests                               #
    #                                                                 #
    ###################################################################

    def test_itemPlaceholder(self):
        pass

    ###################################################################
    #                                                                 #
    #                        Room tests                               #
    #                                                                 #
    ###################################################################

    def test_allRoomsCreated(self):
        """
        Compare the number of room files in the 'Rooms' directory
        to the number of rooms created in an instance of Game.
        """
        dirRooms = len(fnmatch.filter(os.listdir("Rooms"), '*.*'))
        gameRooms = len(self.testGame.rooms)
        self.assertEqual(dirRooms, gameRooms, f"{dirRooms} rooms in "
                                              f"directory - {gameRooms} "
                                              f"rooms in Game instance")

    def test_verifyRoomNameEquality(self):
        """
        Ensure that comparing a room instance to a string accurately matches
        its name attribute.
        """
        for room in self.testGame.rooms:
            self.assertEqual(room, room.name, f"Room ({room.name}) not equal "
                                              f"to string name")

    def test_verifyExpectedRooms(self):
        """
        Ensure that all the rooms created are also the ones
        we EXPECT to be there.
        """
        expectedRooms = [
            "attic",
            "basement",
            "diningRoom",
            "familyRoom",
            "garage",
            "kitchen",
            "lowerHall",
            "masterBedroom",
            "porch",
            "secondBedroom",
            "upperHall",
            "utilityRoom"
        ]

        for roomName in expectedRooms:
            assert roomName in self.testGame.rooms, \
                f"'{roomName}' room does not exist in Game when it should."

    def test_roomExits(self):
        """
        Test whether rooms accurately respond to isValidExit() method
        regardless of spaces or capitalization.
        """
        # In each room, get the valid exits
        for room in self.testGame.rooms:
            for exitName, exitDirection in room.getAllExits().items():
                randName = randomStr(exitName)
                randDir = randomStr(exitDirection)

                # Verify normal name
                self.assertTrue(room.isValidExit(exitName),
                                f"{exitName} should be a "
                                f"valid exit in {room.name}")
                # Verify normal direction
                self.assertTrue(room.isValidExit(exitDirection),
                                f"{exitDirection} should be a "
                                f"valid exit in {room.name}")
                # Verify randomized name
                self.assertTrue(room.isValidExit(randName),
                                f"{randName} should be a "
                                f"valid exit in {room.name}")
                # Verify randomized direction
                self.assertTrue(room.isValidExit(randDir),
                                f"{randDir} should be a "
                                f"valid exit in {room.name}")

    def test_attic(self):
        pass

    def test_basement(self):
        pass

    def test_bathroom(self):
        pass

    def test_diningRoom(self):
        pass

    def test_familyRoom(self):
        pass

    def test_garage(self):
        pass

    def test_kitchen(self):
        pass

    def test_lowerHall(self):
        pass

    def test_masterBedroom(self):
        pass

    def test_porch(self):
        pass

    def test_secondBedroom(self):
        pass

    def test_upperHall(self):
        pass

    def test_utilityRoom(self):
        pass


if __name__ == '__main__':
    unittest.main()
