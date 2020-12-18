from game_rules import MurderEvent, AccusationStatus, UnruledPlayer


def test_accusation():
    """This is the basic rule to define a winner and is done first to prevent depending on too much history"""

    casefile = MurderEvent(room="Kitchen", suspect="Rev Green", weapon="Candlestick")

    p1 = UnruledPlayer()
    p1.accuse("Lounge", "Colonel Mustard", "Rope", casefile)

    assert p1.status == AccusationStatus.WRONG

    p2 = UnruledPlayer()
    p2.accuse("Kitchen", "Rev Green", "Candlestick", casefile)

    assert p2.status == AccusationStatus.CORRECT


def test_suggestion():
    """Tests the suggestion mechanism

    Each player can see the last refuted card

    """

    p1, p2, p3, p4 = (
        UnruledPlayer(room="Lounge"),
        UnruledPlayer(),
        UnruledPlayer(),
        UnruledPlayer(),
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
