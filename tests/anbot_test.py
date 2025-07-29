from anbot.analyze import analyze_sticks, is_only_singles_left, is_parity_state, is_parity_even, is_two_identical_groups_and_one_other, is_one_little_group_and_one_big_group, is_even_number_of_singles
from anbot.think import get_start_of_group, get_group_in_parity_state, get_index_of_first_single, get_group_different_from_the_others
from anbot.do import leave_one_single_from_group, split_group_into_two_singles, take_whole_group, split_group_into_one_single_and_one_group, split_group_into_two_identical_groups, split_group_into_two_different_groups, take_first_single, leave_two_identical_groups
import pytest

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
    with pytest.raises(ValueError):
        get_start_of_group(sticks, 0)

    sticks = [True, True, False, True]
    # Only two groups, so index 2 is out of range
    with pytest.raises(ValueError):
        get_start_of_group(sticks, 2)

    # One big group
    sticks = [True, True, True]
    assert get_start_of_group(sticks, 0) == 0

def test_is_parity_even():
    # Even number of groups: should return True
    assert is_parity_even([2, 1]) == True
    assert is_parity_even([1, 2, 1, 1]) == True

    # Odd number of groups: should return False
    assert is_parity_even([4]) == False
    assert is_parity_even([2, 1, 1]) == False
    assert is_parity_even([1, 3, 1]) == False

def test_get_group_in_parity_state():
    # Only one group, not 1
    assert get_group_in_parity_state([4]) == (0, 4)
    assert get_group_in_parity_state([2]) == (0, 2)
    assert get_group_in_parity_state([3]) == (0, 3)

    # First group is not 1
    assert get_group_in_parity_state([2, 1, 1]) == (0, 2)
    assert get_group_in_parity_state([3, 1, 1]) == (0, 3)

    # Second group is not 1
    assert get_group_in_parity_state([1, 2, 1]) == (1, 2)
    assert get_group_in_parity_state([1, 3, 1]) == (1, 3)

    # Third group is not 1
    assert get_group_in_parity_state([1, 1, 2]) == (2, 2)
    assert get_group_in_parity_state([1, 1, 3]) == (2, 3)

def test_take_whole_group():
    # Test taking the only group
    sticks = [True, True, True]
    move = take_whole_group((0, 3), sticks)
    assert move == (0, 3)

    # Test taking the first group in multiple groups
    sticks = [True, True, False, True, True, True, False, True]
    move = take_whole_group((0, 2), sticks)
    assert move == (0, 2)

    # Test taking the second group
    sticks = [True, True, False, True, True, True, False, True]
    move = take_whole_group((1, 3), sticks)
    assert move == (3, 3)

    # Test taking the last group
    sticks = [True, True, False, True, True, True, False, True]
    move = take_whole_group((2, 1), sticks)
    assert move == (7, 1)

def test_split_group_into_two_singles():
    # Test splitting a group of 3 into two singles
    sticks = [True, True, True]
    move = split_group_into_two_singles((0, 3), sticks)
    assert move == (1, 1)

    # Test splitting a group of 4 into two singles
    sticks = [True, True, True, True]
    move = split_group_into_two_singles((0, 4), sticks)
    assert move == (1, 2)

    # Test splitting a group of 5 into two singles
    sticks = [True, True, True, True, True]
    move = split_group_into_two_singles((0, 5), sticks)
    assert move == (1, 3)

    # Test splitting the second group in a list
    sticks = [True, False, True, True, True, False, True]
    # Groups: [1, 3, 1]
    move = split_group_into_two_singles((1, 3), sticks)
    assert move == (3, 1)

    # Test ValueError for invalid group length (2)
    sticks = [True, True]
    with pytest.raises(ValueError):
        split_group_into_two_singles((0, 2), sticks)

    # Test ValueError for invalid group length (6)
    sticks = [True, True, True, True, True, True]
    with pytest.raises(ValueError):
        split_group_into_two_singles((0, 6), sticks)

def test_leave_one_single_from_group():
    # Test leaving one single from a group of 2
    sticks = [True, True]
    move = leave_one_single_from_group((0, 2), sticks)
    assert move == (0, 1)

    # Test leaving one single from a group of 3
    sticks = [True, True, True]
    move = leave_one_single_from_group((0, 3), sticks)
    assert move == (0, 2)

    # Test leaving one single from a group of 4
    sticks = [True, True, True, True]
    move = leave_one_single_from_group((0, 4), sticks)
    assert move == (0, 3)

    # Test leaving one single from the second group in a list
    sticks = [True, False, True, True, True, False, True]
    # Groups: [1, 3, 1]
    move = leave_one_single_from_group((1, 3), sticks)
    assert move == (2, 2)

    # Test ValueError for invalid group length (1)
    sticks = [True]
    with pytest.raises(ValueError):
        leave_one_single_from_group((0, 1), sticks)

    # Test ValueError for invalid group length (5)
    sticks = [True, True, True, True, True]
    with pytest.raises(ValueError):
        leave_one_single_from_group((0, 5), sticks)

def test_split_group_into_one_single_and_one_group():
    # Test splitting a group of 4
    sticks = [True, True, True, True]
    move = split_group_into_one_single_and_one_group((0, 4), sticks)
    assert move == (1, 1)

    # Test splitting a group of 5
    sticks = [True, True, True, True, True]
    move = split_group_into_one_single_and_one_group((0, 5), sticks)
    assert move == (1, 2)

    # Test splitting a group of 6
    sticks = [True, True, True, True, True, True]
    move = split_group_into_one_single_and_one_group((0, 6), sticks)
    assert move == (1, 3)

    # Test splitting a group of 7
    sticks = [True, True, True, True, True, True, True]
    move = split_group_into_one_single_and_one_group((0, 7), sticks)
    assert move == (1, 3)

    # Test splitting the second group in a list
    sticks = [True, False, True, True, True, True, False, True]
    # Groups: [1, 4, 1]
    move = split_group_into_one_single_and_one_group((1, 4), sticks)
    assert move == (3, 1)

    # Test ValueError for invalid group length (3)
    sticks = [True, True, True]
    with pytest.raises(ValueError):
        split_group_into_one_single_and_one_group((0, 3), sticks)

    # Test ValueError for invalid group length (8)
    sticks = [True] * 8
    with pytest.raises(ValueError):
        split_group_into_one_single_and_one_group((0, 8), sticks)

def test_split_group_into_two_identical_groups():
    # Test splitting a group of 5
    sticks = [True] * 5
    move = split_group_into_two_identical_groups((0, 5), sticks)
    assert move == (2, 1)

    # Test splitting a group of 6
    sticks = [True] * 6
    move = split_group_into_two_identical_groups((0, 6), sticks)
    assert move == (2, 2)

    # Test splitting a group of 7
    sticks = [True] * 7
    move = split_group_into_two_identical_groups((0, 7), sticks)
    assert move == (3, 1)

    # Test splitting a group of 8
    sticks = [True] * 8
    move = split_group_into_two_identical_groups((0, 8), sticks)
    assert move == (3, 2)

    # Test splitting the third group in a list
    sticks = [True, False, True, True, True, True, False, True, True, True, True, True]
    # Groups: [1, 4, 5]
    move = split_group_into_two_identical_groups((2, 5), sticks)
    assert move == (9, 1)

    # Test ValueError for invalid group length (4)
    sticks = [True] * 4
    with pytest.raises(ValueError):
        split_group_into_two_identical_groups((0, 4), sticks)

    # Test ValueError for invalid group length (9)
    sticks = [True] * 9
    with pytest.raises(ValueError):
        split_group_into_two_identical_groups((0, 9), sticks)

def test_split_group_into_two_different_groups():
    # Test splitting a group of 6
    sticks = [True] * 6
    move = split_group_into_two_different_groups((0, 6), sticks)
    assert move == (2, 1)

    # Test splitting a group of 7
    sticks = [True] * 7
    move = split_group_into_two_different_groups((0, 7), sticks)
    assert move == (2, 2)

    # Test splitting a group of 8
    sticks = [True] * 8
    move = split_group_into_two_different_groups((0, 8), sticks)
    assert move == (2, 3)

    # Test splitting the second group in a list
    sticks = [True, False, True, True, True, True, True, True, True, False, True, True]
    # Groups: [1, 7, 2]
    move = split_group_into_two_different_groups((1, 7), sticks)
    assert move == (4, 2)

    # Test ValueError for invalid group length (4)
    sticks = [True] * 4
    with pytest.raises(ValueError):
        split_group_into_two_different_groups((0, 4), sticks)

    # Test ValueError for invalid group length (9)
    sticks = [True] * 9
    with pytest.raises(ValueError):
        split_group_into_two_different_groups((0, 9), sticks)

def test_get_index_of_first_single():
    # Single stick at start
    sticks = [True, False, False, False]
    assert get_index_of_first_single(sticks) == 0

    # Single stick at end
    sticks = [False, False, False, True]
    assert get_index_of_first_single(sticks) == 3

    # Single stick in the middle
    sticks = [False, True, False, False]
    assert get_index_of_first_single(sticks) == 1

    # Multiple singles, should return the first
    sticks = [False, True, False, True, False, True]
    assert get_index_of_first_single(sticks) == 1

    # No singles (all taken)
    sticks = [False, False, False]
    with pytest.raises(ValueError):
        get_index_of_first_single(sticks)

    # No singles (all sticks together)
    sticks = [True, True, True]
    with pytest.raises(ValueError):
        get_index_of_first_single(sticks)

def test_take_first_single():
    # Single stick at start
    sticks = [True, False, False, False]
    assert take_first_single(sticks) == (0, 1)

    # Single stick at end
    sticks = [False, False, False, True]
    assert take_first_single(sticks) == (3, 1)

    # Single stick in the middle
    sticks = [False, True, False, False]
    assert take_first_single(sticks) == (1, 1)

    # Multiple singles, should return the first
    sticks = [False, True, False, True, False, True]
    assert take_first_single(sticks) == (1, 1)

    # No singles (all taken)
    sticks = [False, False, False]
    with pytest.raises(ValueError):
        take_first_single(sticks)

    # No singles (all sticks together)
    sticks = [True, True, True]
    with pytest.raises(ValueError):
        take_first_single(sticks)

def test_is_two_identical_groups_and_one_other():
    # Two groups of 2, one group of 3 (should be True)
    assert is_two_identical_groups_and_one_other([2, 2, 3]) is True

    # Two groups of 3, one group of 5 (should be True)
    assert is_two_identical_groups_and_one_other([3, 3, 5]) is True

    # Two groups of 2, one group of 4 (should be True)
    assert is_two_identical_groups_and_one_other([2, 2, 4]) is True

    # Two groups of 3, one single (should be True)
    assert is_two_identical_groups_and_one_other([3, 3, 1]) is True

    # Only singles (should be False)
    assert is_two_identical_groups_and_one_other([1, 1, 1]) is False

    # Three different sizes (should be False)
    assert is_two_identical_groups_and_one_other([2, 1, 3]) is False

    # More than three groups (should be False)
    assert is_two_identical_groups_and_one_other([2, 2, 1, 1]) is False

    # Less than three groups (should be False)
    assert is_two_identical_groups_and_one_other([2, 2]) is False

    # Group greater than 5 (should be False)
    assert is_two_identical_groups_and_one_other([6, 2, 2]) is False

def test_get_group_different_from_the_others():
    # All groups equal
    assert get_group_different_from_the_others([2, 2, 2]) == (0, 2)
    assert get_group_different_from_the_others([1, 1, 1]) == (0, 1)
    assert get_group_different_from_the_others([3, 3, 3]) == (0, 3)

    # First two equal, third different
    assert get_group_different_from_the_others([2, 2, 3]) == (2, 3)
    assert get_group_different_from_the_others([1, 1, 2]) == (2, 2)
    assert get_group_different_from_the_others([3, 3, 1]) == (2, 1)

    # First and last equal, middle different
    assert get_group_different_from_the_others([2, 3, 2]) == (1, 3)
    assert get_group_different_from_the_others([1, 2, 1]) == (1, 2)
    assert get_group_different_from_the_others([3, 1, 3]) == (1, 1)

    # Last two equal, first different
    assert get_group_different_from_the_others([3, 2, 2]) == (0, 3)
    assert get_group_different_from_the_others([2, 1, 1]) == (0, 2)
    assert get_group_different_from_the_others([1, 3, 3]) == (0, 1)

    # More than three groups should raise ValueError
    with pytest.raises(ValueError):
        get_group_different_from_the_others([1, 1, 1, 1])

    # Less than three groups: function expects exactly three, so unpacking will fail
    with pytest.raises(ValueError):
        get_group_different_from_the_others([1, 2])

def test_leave_two_identical_groups():
    # Two identical groups and one different, different is first (group_length=3)
    groups = [3, 2, 2]
    sticks = [True, True, True, False, True, True, False, True, True]
    assert leave_two_identical_groups(groups, sticks) == (0, 3)

    # Two identical groups and one different, different is last (group_length=3)
    groups = [2, 2, 3]
    sticks = [True, True, False, True, True, False, True, True, True]
    assert leave_two_identical_groups(groups, sticks) == (6, 3)

    # Two identical groups and one different, different is middle (group_length=3)
    groups = [2, 3, 2]
    sticks = [True, True, False, True, True, True, False, True, True]
    assert leave_two_identical_groups(groups, sticks) == (3, 3)

    # All groups identical (should return the first group)
    groups = [1, 1, 1]
    sticks = [True, False, True, False, True]
    assert leave_two_identical_groups(groups, sticks) == (0, 1)

    # group_length=4 (should split group into two singles)
    groups = [4, 2, 2]
    sticks = [True, True, True, True, False, True, True, False, True, True]
    assert leave_two_identical_groups(groups, sticks) == (1, 2)

    # group_length=5 (should split group into two singles)
    groups = [2, 2, 5]
    sticks = [True, True, False, True, True, False, True, True, True, True, True]
    assert leave_two_identical_groups(groups, sticks) == (7, 3)

    # Should raise ValueError if not exactly three groups
    with pytest.raises(ValueError):
        leave_two_identical_groups([2, 2], [True, True, False, True, True])
    with pytest.raises(ValueError):
        leave_two_identical_groups([1, 1, 1, 1], [True, False, True, False, True, False, True])

def test_is_one_little_group_and_one_big_group():
    # Valid cases: little group = 2, big group = 3, 4, 5
    assert is_one_little_group_and_one_big_group([2, 3]) is True
    assert is_one_little_group_and_one_big_group([3, 2]) is True
    assert is_one_little_group_and_one_big_group([2, 4]) is True
    assert is_one_little_group_and_one_big_group([4, 2]) is True
    assert is_one_little_group_and_one_big_group([2, 5]) is True
    assert is_one_little_group_and_one_big_group([5, 2]) is True

    # Valid cases: little group = 3, big group = 4, 5, 6
    assert is_one_little_group_and_one_big_group([3, 4]) is True
    assert is_one_little_group_and_one_big_group([4, 3]) is True
    assert is_one_little_group_and_one_big_group([3, 5]) is True
    assert is_one_little_group_and_one_big_group([5, 3]) is True
    assert is_one_little_group_and_one_big_group([3, 6]) is True
    assert is_one_little_group_and_one_big_group([6, 3]) is True

    # Invalid: both groups too small
    assert is_one_little_group_and_one_big_group([1, 2]) is False
    assert is_one_little_group_and_one_big_group([2, 1]) is False
    assert is_one_little_group_and_one_big_group([1, 3]) is False
    assert is_one_little_group_and_one_big_group([3, 1]) is False

    # Invalid: both groups too big
    assert is_one_little_group_and_one_big_group([4, 5]) is False
    assert is_one_little_group_and_one_big_group([5, 4]) is False
    assert is_one_little_group_and_one_big_group([5, 6]) is False
    assert is_one_little_group_and_one_big_group([6, 5]) is False

    # Invalid: both groups equal
    assert is_one_little_group_and_one_big_group([2, 2]) is False
    assert is_one_little_group_and_one_big_group([3, 3]) is False
    assert is_one_little_group_and_one_big_group([4, 4]) is False

    # Invalid: more than two groups
    assert is_one_little_group_and_one_big_group([2, 3, 4]) is False
    assert is_one_little_group_and_one_big_group([1, 2, 3]) is False

    # Invalid: less than two groups
    assert is_one_little_group_and_one_big_group([2]) is False
    assert is_one_little_group_and_one_big_group([]) is False

def test_is_even_number_of_singles():
    # Even number of singles
    assert is_even_number_of_singles([1, 1]) is True
    assert is_even_number_of_singles([1, 1, 1, 1]) is True
    assert is_even_number_of_singles([1, 1, 1, 1, 1, 1]) is True

    # Odd number of singles
    assert is_even_number_of_singles([1]) is False
    assert is_even_number_of_singles([1, 1, 1]) is False
    assert is_even_number_of_singles([1, 1, 1, 1, 1]) is False

    # Mixed groups with even number of singles
    assert is_even_number_of_singles([1, 2, 1]) is True
    assert is_even_number_of_singles([2, 1, 1, 3]) is True
    assert is_even_number_of_singles([1, 4, 1, 2]) is True

    # Mixed groups with odd number of singles
    assert is_even_number_of_singles([1, 2]) is False
    assert is_even_number_of_singles([2, 1, 1, 3, 1]) is False
    assert is_even_number_of_singles([1, 4, 1, 2, 1]) is False

    # No singles (all groups > 1)
    assert is_even_number_of_singles([2, 3]) is False
    assert is_even_number_of_singles([2, 3, 4]) is False
    assert is_even_number_of_singles([2]) is False