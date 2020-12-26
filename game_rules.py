from dataclasses import dataclass
from uuid import uuid4


@dataclass
class MurderEvent:
    room: str
    weapon: str
    suspect: str


from enum import Enum


class State(str, Enum):
    ONROOM = "on_room"
    ONCORRIDOR = "on_corridor"
    ILLEGAL = "illegal"
    WON = "won"
    LOST = "lost"


@dataclass
class Player:
    """This is basic suggestion/accusation behaviour as in last page of rules.

    It does not check pre-conditions of pawns position, whose turn ist, etc. Its very raw and unruled."""

    def __init__(self, state=State.ONCORRIDOR, room=None, cards=[], position=None):
        self.cards = set(cards)
        self.cards_to_check = {}
        self.last_card_refuted = None
        self.room = room
        self.__hash = uuid4().int
        self.state = state
        self.position = position

    def accuse(self, room, suspect, weapon):
        if not (self.state in [State.ONROOM, State.ONCORRIDOR]):
            self.state = State.ILLEGAL
            return self

        self.accusation = MurderEvent(room, weapon, suspect)
        return self

    def check_accusation(self, casefile):
        if self.state == State.ILLEGAL:
            self.state = State.ILLEGAL
            return
        if self.accusation == casefile:
            self.state = State.WON
        else:
            self.state = State.LOST

    def receive_cards(self, cards):
        self.cards.update(cards)

    def enter_room(self, room, strict=True):
        """This sets the room for suggestions.
        Strict parameter controls pre conditions like being on rooms door or having a real shortcut
        """
        if self._position == RoomDoor(room) or strict == False:
            self.room = room
            self.position = room
            self.state = State.ONROOM
        elif has_shortcut(self._position, room):
            self.room = room
            self.position = room
            self.state = State.ONROOM
        else:
            self.state = State.ILLEGAL
        return self

    def suggest(self, suspect, weapon):
        """Player suggesions can only relate to the room he is in"""
        self.suggestion = MurderEvent(self.room, suspect, weapon)

    def check_suggestion(self, other):
        suggestion_as_set = set(
            [self.suggestion.room, self.suggestion.suspect, self.suggestion.weapon]
        )
        other._receive_check_suggestion(self, suggestion_as_set)

    def _receive_check_suggestion(self, other, suggestion):
        self.cards_to_check[other] = suggestion.intersection(self.cards)

    def confirm_check_suggestion(self, other, card=None):
        if len(self.cards_to_check[other]) != 0:
            try:
                self.cards_to_check[other].remove(card)
                other.last_card_refuted = card
            except KeyError as e:
                raise Exception("Tried to refute an irrefutable card")

    def __hash__(self):
        return self.__hash

    @property
    def position(self):
        if type(self._position) != RoomDoor:
            return self._position
        else:
            pass

    @position.setter
    def position(self, value):
        self._position = value


@dataclass
class RoomDoor:
    room: str


def has_shortcut(from_room, to_room):
    if (from_room, to_room) == ("Kitchen", "Study"):
        return True
    else:
        pass
