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

    p1 = Player(state=State.ONCORRIDOR, position="Kitchen").enter_room("Study")
    assert p1.state == State.ONROOM
    assert p1.position == "Study"

    p2 = Player(state=State.ONCORRIDOR, position="Study").enter_room("Kitchen")
    assert p2.state == State.ONROOM
    assert p2.position == "Kitchen"

    p3 = Player(state=State.ONCORRIDOR, position="Lounge").enter_room("Conservatory")
    assert p3.state == State.ONROOM
    assert p3.position == "Conservatory"

    p4 = Player(state=State.ONCORRIDOR, position="Conservatory").enter_room("Lounge")
    assert p4.state == State.ONROOM
    assert p4.position == "Lounge"


def test_shortcut_invalid():
    assert (
        Player(state=State.ONCORRIDOR, position="Kitchen").enter_room("Attic").state
        == State.ILLEGAL
    )


def test_leave_room():

    p1 = Player(state=State.ONROOM, position="Kitchen")
    p1.leave_room()
    assert p1.state == State.ONCORRIDOR
    assert p1.position == RoomDoor("Kitchen")
