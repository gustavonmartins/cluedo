from game_rules import MurderEvent, Player
import pytest
from conftest import load_json_data


jsonpath = "test_data_accusation.json"


@pytest.fixture(name="testset", params=load_json_data(jsonpath))
def fixture_testset(request):
    return request.param


def test_accuse(testset):
    """Tests winning and loosing accusations.

    Inputs and expected results are read from json json file"""

    from_state = testset["from_state"]
    room = testset["room"]
    suspect = testset["suspect"]
    weapon = testset["weapon"]
    result = testset["result"]

    casefile = MurderEvent(room="Kitchen", suspect="Rev Green", weapon="Candlestick")

    p1 = Player(state=from_state)
    p1.accuse(room, suspect, weapon).check_accusation(casefile)

    assert p1.state == result


def test_suggestion():
    """Tests the suggestion mechanism

    Each player can see the last refuted card

    """

    p1, p2, p3, p4 = (
        Player(position="Lounge"),
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

    p1.enter_room("Kitchen", strict=False).suggest("Colonel Mustard", "Dagger")
    p1.check_suggestion(p2)
    p2.confirm_check_suggestion(p1, "Dagger")
    assert p1.last_card_refuted == "Dagger"

    p1.enter_room("Bathroom", strict=False).suggest("Colonel Mustard", "Dagger")
    p3.enter_room("Kitchen", strict=False).suggest("Rev Green", "Pipe")
    p3.check_suggestion(p2)
    p1.check_suggestion(p2)
    p2.confirm_check_suggestion(p1, "Dagger")
    p2.confirm_check_suggestion(p3, "Kitchen")
    assert p1.last_card_refuted == "Dagger"
    assert p3.last_card_refuted == "Kitchen"
