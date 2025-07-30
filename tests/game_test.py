from game.game import create_sticks_from_groups, display_sticks, is_game_over, is_valid_move, remove_sticks

def test_is_game_over():
    # All sticks present
    sticks = [True] * 16
    assert not is_game_over(sticks)
    # All sticks removed
    sticks = [False] * 16
    assert is_game_over(sticks)
    # Some sticks present
    sticks = [False, True, False, False]
    assert not is_game_over(sticks)
    # No sticks (empty list)
    sticks = []
    assert is_game_over(sticks)

def test_is_valid_move():
    sticks = [True] * 5
    # Valid moves
    assert is_valid_move(sticks, (0, 1))
    assert is_valid_move(sticks, (1, 2))
    assert is_valid_move(sticks, (2, 3))
    # Invalid count
    assert not is_valid_move(sticks, (0, 0))
    assert not is_valid_move(sticks, (0, 4))
    # Out of bounds
    assert not is_valid_move(sticks, (-1, 1))
    assert not is_valid_move(sticks, (4, 2))
    # Not all sticks available
    sticks2 = [True, False, True, True, True]
    assert not is_valid_move(sticks2, (0, 2))  # includes a False
    assert is_valid_move(sticks2, (2, 2))      # both True

    sticks = [True, True, False, True, True]
    # Try to take over a removed stick
    assert not is_valid_move(sticks, (1, 3))  # includes False at index 2
    # Valid move at the end
    assert is_valid_move(sticks, (3, 2))
    # Valid move at the start
    assert is_valid_move(sticks, (0, 2))
    
def test_remove_sticks():
    sticks = [True, True, True, True, True]
    remove_sticks(sticks, (1, 3))
    assert sticks == [True, False, False, False, True]
    # Remove at start
    remove_sticks(sticks, (0, 1))
    assert sticks == [False, False, False, False, True]
    # Remove at end
    remove_sticks(sticks, (4, 1))
    assert sticks == [False, False, False, False, False]

def test_display_sticks(capsys):
    sticks = [True, False, True, True]
    display_sticks(sticks)
    captured = capsys.readouterr()
    # Should print stick and number lines
    assert "|" in captured.out
    assert "1" in captured.out
    assert "3" in captured.out
    # Check that removed stick is blank
    assert "2" not in captured.out

def test_create_sticks_from_groups():
    # Test with three groups: (3, 2, 1)
    groups = [3, 2, 1]
    sticks = create_sticks_from_groups(groups)
    assert sticks == [True, True, True, False, True, True, False, True, False]

    # Test with one group: (4)
    groups = [4]
    sticks = create_sticks_from_groups(groups)
    assert sticks == [True, True, True, True, False]

    # Test with two groups: (2, 2)
    groups = [2, 2]
    sticks = create_sticks_from_groups(groups)
    assert sticks == [True, True, False, True, True, False]

    # Test with empty groups
    groups = []
    sticks = create_sticks_from_groups(groups)
    assert sticks == []

    # Test with group of size 1
    groups = [1]
    sticks = create_sticks_from_groups(groups)
    assert sticks == [True, False]