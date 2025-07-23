from anbot.anbot import analyze_sticks, only_singles_left

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
    assert only_singles_left([1]) == True

    # Multiple groups of 1
    assert only_singles_left([1, 1, 1]) == True

    # Group with more than 1
    assert only_singles_left([2]) == False
    assert only_singles_left([1, 2]) == False
    assert only_singles_left([2, 1]) == False

    # Empty list (no groups)
    assert only_singles_left([]) == True

    # Mixed groups
    assert only_singles_left([1, 3, 1]) == False