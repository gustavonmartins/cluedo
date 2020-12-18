from dataclasses import dataclass


@dataclass
class CaseFile:
    room: str
    weapon: str
    suspect: str


@dataclass
class Accusation:
    room: str
    suspect: str
    weapon: str


def accuse(room, suspect, weapon) -> Accusation:
    return Accusation(room=room, weapon=weapon, suspect=suspect)


def check_accusation(accusation, casefile):
    if (
        (accusation.room == casefile.room)
        and (accusation.suspect == casefile.suspect)
        and (accusation.weapon == casefile.weapon)
    ):
        return True
    else:
        return False
