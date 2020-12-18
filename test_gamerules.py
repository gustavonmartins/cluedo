from game_rules import MurderEvent, PlayerStatus, Player


def test_accusation():
    """This is the basic rule to define a winner and is done first to prevent depending on too much history"""

    casefile = MurderEvent(room="Kitchen", suspect="Rev Green", weapon="Candlestick")

    p1 = Player()
    p1.accuse("Lounge", "Colonel Mustard", "Rope", casefile)

    assert p1.status == PlayerStatus.LOST

    p2 = Player()
    p2.enter_room("Hall").accuse("Kitchen", "Rev Green", "Candlestick", casefile)

    assert p2.status == PlayerStatus.WON
