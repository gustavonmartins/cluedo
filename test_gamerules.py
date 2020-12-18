from game_basics import CaseFile, accuse, accuse, check_accusation


def test_accusation():
    """This is the basic rule to define a winner and is done first to prevent depending on too much history"""
    casefile = CaseFile(room="Kitchen", suspect="Rev Green", weapon="Candlestick")
    accusation = accuse(room="Lounge", suspect="Colonen Mustard", weapon="Rope")
    correct_accusation = accuse(
        room="Kitchen", suspect="Rev Green", weapon="Candlestick"
    )

    assert check_accusation(accusation, casefile) == False
    assert check_accusation(correct_accusation, casefile) == True
