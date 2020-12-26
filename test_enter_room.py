from game_rules import Player, State, RoomDoor


def test_enterroom_valid():
    """Tests player entering valid and invalid rooms"""
    p1 = Player(state=State.ONCORRIDOR, position=RoomDoor("Kitchen"))
    p1.enter_room("Kitchen")
    assert p1.position == "Kitchen"
    assert p1.state == State.ONROOM


def test_enterroom_invalid():
    p1 = Player(state=State.ONCORRIDOR, position="Kitchen")
    p1.enter_room("Attic")
    assert p1.state == State.ILLEGAL

    p2 = Player(state=State.ONCORRIDOR, position=RoomDoor("Kitchen"))
    p2.enter_room("Attic")
    assert p1.state == State.ILLEGAL

    p3 = Player(state=State.ONCORRIDOR, position="A7")
    p3.enter_room("Attic")
    assert p3.state == State.ILLEGAL


def test_entershortcut_valid():
    """Test players using shortcuts"""

    p1 = Player(state=State.ONCORRIDOR, position="Kitchen")
    p1.enter_room("Study")
    assert p1.state == State.ONROOM
    assert p1.position == "Study"


def test_shortcut_invalid():
    p1 = Player(state=State.ONCORRIDOR, position="Kitchen")
    p1.enter_room("Attic")
    assert p1.state == State.ILLEGAL
