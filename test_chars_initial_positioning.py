from game_rules import Player, State


def test_initial_positioning():
    initial_pos = {
        "Mrs. Peacock": (1, 7),
        "Mr. Green": (10, 1),
        "Mrs. White": (15, 1),
        "Prof. Plum": (1, 20),
        "Miss Scarlett": (17, 25),
        "Col. Mustard": (18, 24),
    }
    for char, v in initial_pos.items():
        player = Player(character=char)
        player.start_initial_position()
        assert player.state == State.ONCORRIDOR
        assert player.position == v
