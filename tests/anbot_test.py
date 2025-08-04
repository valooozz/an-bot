import pytest
from anbot.analyze import analyze_sticks, is_exact_groups, is_n_identical_groups, is_one_group_left, is_only_singles_left, is_parity_state
from anbot.singles import get_groups_without_pairs_of_singles, get_number_of_singles, remove_singles

# ============================== analyze.py ============================== # 

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

    # One group of 5: parity state
    assert is_parity_state([5]) == True

    # One group of 6: not a parity state
    assert is_parity_state([6]) == False

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

def test_is_exact_group():
    # Exact match, same order
    assert is_exact_groups([1, 2, 3], [1, 2, 3]) == True

    # Exact match, different order (should be sorted)
    assert is_exact_groups([3, 2, 1], [1, 2, 3]) == True

    # Not exact: different values
    assert is_exact_groups([1, 2, 4], [1, 2, 3]) == False

    # Not exact: different lengths
    assert is_exact_groups([1, 2], [1, 2, 3]) == False
    assert is_exact_groups([1, 2, 3, 4], [1, 2, 3]) == False

    # Both empty
    assert is_exact_groups([], []) == True

    # One empty, one not
    assert is_exact_groups([], [1]) == False
    assert is_exact_groups([1], []) == False

    # Duplicates
    assert is_exact_groups([2, 2, 3, 3], [2, 2, 3, 3]) == True
    assert is_exact_groups([2, 3, 2, 3], [2, 2, 3, 3]) == True
    assert is_exact_groups([2, 3, 3], [2, 2, 3, 3]) == False

def test_is_n_identical_groups():
    # All groups are identical and length matches n
    assert is_n_identical_groups([2, 2], 2) == True
    assert is_n_identical_groups([3, 3, 3], 3) == True
    assert is_n_identical_groups([1], 1) == True

    # Not all groups are identical
    assert is_n_identical_groups([2, 3], 2) == False
    assert is_n_identical_groups([3, 3, 2], 3) == False

    # Length does not match n
    assert is_n_identical_groups([2, 2, 2], 2) == False
    assert is_n_identical_groups([1], 2) == False
    assert is_n_identical_groups([], 1) == False

def test_is_one_group_left():
    # One group left
    assert is_one_group_left([3]) == True
    assert is_one_group_left([1]) == True
    assert is_one_group_left([10]) == True

    # More than one group
    assert is_one_group_left([1, 2]) == False
    assert is_one_group_left([2, 2, 2]) == False

    # No groups
    assert is_one_group_left([]) == False

# ============================== singles.py ============================== # 

def test_get_number_of_singles():
    # No singles
    assert get_number_of_singles([2, 3, 4]) == 0

    # All singles
    assert get_number_of_singles([1, 1, 1]) == 3

    # Mixed groups
    assert get_number_of_singles([1, 2, 1, 3, 1]) == 3

    # One single
    assert get_number_of_singles([1]) == 1

    # Empty list
    assert get_number_of_singles([]) == 0

def test_remove_singles():
    # No singles to remove
    assert remove_singles([2, 3, 4], True) == [2, 3, 4]
    assert remove_singles([2, 3, 4], False) == [2, 3, 4]

    # All singles, accept_one True: keep one single
    assert remove_singles([1, 1, 1], True) == [1]
    assert remove_singles([1], True) == [1]
    assert remove_singles([1, 1], False) == []

    # Mixed groups, accept_one True: keep first single, keep non-singles
    assert remove_singles([1, 2, 1, 3, 1], True) == [1, 2, 3]
    assert remove_singles([2, 1, 3, 1], True) == [2, 1, 3]
    assert remove_singles([2, 3, 1], True) == [2, 3, 1]
    assert remove_singles([1, 2, 3], True) == [1, 2, 3]

    # Mixed groups, accept_one False: remove all singles, keep non-singles
    assert remove_singles([1, 2, 1, 3, 1], False) == [2, 3]
    assert remove_singles([2, 1, 3, 1], False) == [2, 3]
    assert remove_singles([2, 3, 1], False) == [2, 3]
    assert remove_singles([1, 2, 3], False) == [2, 3]

    # No groups
    assert remove_singles([], True) == []
    assert remove_singles([], False) == []

def test_get_groups_without_pairs_of_singles():
    # No singles
    assert get_groups_without_pairs_of_singles([2, 3, 4]) == [2, 3, 4]

    # All singles (odd number): keep one single
    assert get_groups_without_pairs_of_singles([1, 1, 1]) == [1]
    assert get_groups_without_pairs_of_singles([1]) == [1]

    # All singles (even number): remove all
    assert get_groups_without_pairs_of_singles([1, 1]) == []
    assert get_groups_without_pairs_of_singles([1, 1, 1, 1]) == []

    # Mixed groups, odd number of singles: keep one single, keep non-singles
    assert get_groups_without_pairs_of_singles([1, 2, 1, 3, 1]) == [1, 2, 3]
    assert get_groups_without_pairs_of_singles([2, 1, 3, 1, 1]) == [2, 1, 3]
    assert get_groups_without_pairs_of_singles([2, 3, 1]) == [2, 3, 1]
    assert get_groups_without_pairs_of_singles([1, 2, 3]) == [1, 2, 3]

    # Mixed groups, even number of singles: remove all singles, keep non-singles
    assert get_groups_without_pairs_of_singles([1, 2, 1, 3]) == [2, 3]
    assert get_groups_without_pairs_of_singles([2, 1, 3, 1]) == [2, 3]
    assert get_groups_without_pairs_of_singles([2, 3, 1, 1]) == [2, 3]
    assert get_groups_without_pairs_of_singles([1, 2, 3, 1]) == [2, 3]

    # No groups
    assert get_groups_without_pairs_of_singles([]) == []