from dataclasses import dataclass


@dataclass
class MurderEvent:
    room: str
    weapon: str
    suspect: str


from enum import Enum


class PlayerStatus(Enum):
    WON = "Won"
    LOST = "Lost"
    PLAYING = "Playing"


@dataclass
class Player:
    def __init__(self, room=None, status=PlayerStatus.PLAYING):
        self.room = room
        self.status = status

    def accuse(self, room, suspect, weapon, casefile):
        accusation = MurderEvent(room, weapon, suspect)
        if accusation == casefile:
            self.status = PlayerStatus.WON
        else:
            self.status = PlayerStatus.LOST

    def enter_room(self, room):
        self.room = room
        return self
