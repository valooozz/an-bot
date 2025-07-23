from anbot.analyze import analyze_sticks, is_only_singles_left, is_parity_state
from anbot.think import get_start_of_group

def test_analyze_sticks():
    # Test with all sticks present
    assert analyze_sticks([True]*16) == [16]

    # Test with all sticks removed
    assert analyze_sticks([False]*16) == []

    # Test with one group in the middle
    sticks = [False, True, True, True, False]
    assert analyze_sticks(sticks) == [3]

    # Test with several groups
    sticks = [True, True, False, True, True, True, False, True]
    assert analyze_sticks(sticks) == [2, 3, 1]

    # Test with alternating sticks
    sticks = [True, False, True, False, True]
    assert analyze_sticks(sticks) == [1, 1, 1]

    # Test with single stick
    sticks = [True]
    assert analyze_sticks(sticks) == [1]

    # Test with single stick removed
    sticks = [False]
    assert analyze_sticks(sticks) == []

    # Test with group at the end
    sticks = [False, False, True, True]
    assert analyze_sticks(sticks) == [2]

    # Test with group at the start
    sticks = [True, True, False, False]
    assert analyze_sticks(sticks) == [2]

def test_only_singles_left():
    # Only single group of 1
    assert is_only_singles_left([1]) == True

    # Multiple groups of 1
    assert is_only_singles_left([1, 1, 1]) == True

    # Group with more than 1
    assert is_only_singles_left([2]) == False
    assert is_only_singles_left([1, 2]) == False
    assert is_only_singles_left([2, 1]) == False

    # Empty list (no groups)
    assert is_only_singles_left([]) == True

    # Mixed groups
    assert is_only_singles_left([1, 3, 1]) == False

def test_is_parity_state():
    # Only singles: not a parity state
    assert is_parity_state([1, 1, 1]) == False

    # One group of 2, rest singles: parity state
    assert is_parity_state([1, 2, 1]) == True
    assert is_parity_state([2, 1, 1]) == True
    assert is_parity_state([1, 1, 2]) == True

    # One group of 3, rest singles: parity state
    assert is_parity_state([1, 3, 1]) == True
    assert is_parity_state([3, 1, 1]) == True
    assert is_parity_state([1, 1, 3]) == True

    # One group of 4, rest singles: parity state
    assert is_parity_state([1, 4, 1]) == True
    assert is_parity_state([4, 1, 1]) == True
    assert is_parity_state([1, 1, 4]) == True

    # Two groups of 2: not a parity state
    assert is_parity_state([2, 2]) == False

    # One group of 5: not a parity state
    assert is_parity_state([5]) == False

    # Group of 2 and group of 3: not a parity state
    assert is_parity_state([2, 3]) == False

    # Empty list: not a parity state (no groups)
    assert is_parity_state([]) == False

    # One group of 2: parity state
    assert is_parity_state([2]) == True

    # One group of 3: parity state
    assert is_parity_state([3]) == True

    # One group of 4: parity state
    assert is_parity_state([4]) == True

def test_get_start_of_group():
    sticks = [True, True, False, True, False, True, True, True]
    # Groups: [2, 1, 3]
    assert get_start_of_group(sticks, 0) == 0  # First group starts at 0
    assert get_start_of_group(sticks, 1) == 3  # Second group starts at 3
    assert get_start_of_group(sticks, 2) == 5  # Third group starts at 5

    # Single group at start
    sticks = [True, False, False, False]
    assert get_start_of_group(sticks, 0) == 0

    # Single group at end
    sticks = [False, False, True]
    assert get_start_of_group(sticks, 0) == 2

    # All sticks taken (no groups) - should raise
    sticks = [False, False, False]
    try:
        get_start_of_group(sticks, 0)
        assert False, "Expected ValueError for no groups"
    except ValueError:
        pass

    # Index out of range - should raise
    sticks = [True, True, False, True]
    # Only two groups, so index 2 is out of range
    try:
        get_start_of_group(sticks, 2)
        assert False, "Expected ValueError for group index out of range"
    except ValueError:
        pass

    # One big group
    sticks = [True, True, True]
    assert get_start_of_group(sticks, 0) == 0