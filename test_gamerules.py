from game_rules import MurderEvent, AccusationStatus, Player
from pytest import mark


@mark.parametrize(
    "from_state, room, suspect, weapon, result",
    [
        (
            AccusationStatus.ONROOM,
            "Lounge",
            "Colonel Mustard",
            "Rope",
            AccusationStatus.WRONG,
        ),
        (
            AccusationStatus.ONROOM,
            "Kitchen",
            "Rev Green",
            "Candlestick",
            AccusationStatus.CORRECT,
        ),
        (
            AccusationStatus.ONCORRIDOR,
            "Lounge",
            "Colonel Mustard",
            "Rope",
            AccusationStatus.WRONG,
        ),
        (
            AccusationStatus.ONCORRIDOR,
            "Kitchen",
            "Rev Green",
            "Candlestick",
            AccusationStatus.CORRECT,
        ),
        (
            AccusationStatus.WRONG,
            "Kitchen",
            "Rev Green",
            "Candlestick",
            AccusationStatus.ILLEGAL,
        ),
    ],
)
def test_accuse(from_state, room, suspect, weapon, result):
    """Tests winning and loosing accusations"""

    casefile = MurderEvent(room="Kitchen", suspect="Rev Green", weapon="Candlestick")

    p1 = Player(state=from_state)
    p1.accuse(room, suspect, weapon).check_accusation(casefile)

    assert p1.state == result


def test_suggestion():
    """Tests the suggestion mechanism

    Each player can see the last refuted card

    """

    p1, p2, p3, p4 = (
        Player(room="Lounge"),
        Player(),
        Player(),
        Player(),
    )

    p2.receive_cards(["Kitchen", "Colonel Mustard", "Dagger"])
    p3.receive_cards(["Leisure room", "Mr. Black", "Knife"])
    p4.receive_cards(["Lounge", "Rev Green", "Knife"])

    p1.suggest("Rev Green", "Candlestick")

    p1.check_suggestion(p2)
    p2.confirm_check_suggestion(p1)

    p1.check_suggestion(p3)
    p3.confirm_check_suggestion(p1)

    p1.check_suggestion(p4)
    p4.confirm_check_suggestion(p1, "Rev Green")
    assert p1.last_card_refuted == "Rev Green"

    p1.enter_room("Kitchen").suggest("Colonel Mustard", "Dagger")
    p1.check_suggestion(p2)
    p2.confirm_check_suggestion(p1, "Dagger")
    assert p1.last_card_refuted == "Dagger"

    p1.enter_room("Bathroom").suggest("Colonel Mustard", "Dagger")
    p3.enter_room("Kitchen").suggest("Rev Green", "Pipe")
    p3.check_suggestion(p2)
    p1.check_suggestion(p2)
    p2.confirm_check_suggestion(p1, "Dagger")
    p2.confirm_check_suggestion(p3, "Kitchen")
    assert p1.last_card_refuted == "Dagger"
    assert p3.last_card_refuted == "Kitchen"
