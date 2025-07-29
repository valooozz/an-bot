from anbot.think import get_index_of_first_single, get_start_of_group
from game.game import log
from game_types.game_types import GroupPosition, Groups, Move, Sticks

def take_first_single(sticks: Sticks) -> Move:
    log('Take first single')
    first_single_index = get_index_of_first_single(sticks)
    return (first_single_index, 1)

def take_whole_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    log('Take whole group')
    group_index, group_length = group_position
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length)

def split_group_into_two_singles(group_position: GroupPosition, sticks: Sticks) -> Move:
    log('Split group into two singles')
    group_index, group_length = group_position
    if group_length not in (3, 4, 5):
        raise ValueError("Can only split groups of length 3, 4, or 5 into two singles")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 1, group_length - 2)

def leave_one_single_from_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    log('Leave one single from group')
    group_index, group_length = group_position
    if group_length not in (2, 3, 4):
        raise ValueError("Can only leave one single from groups of length 2, 3, or 4")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length - 1)

def split_group_into_one_single_and_one_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    log('Split group into one single and one group')
    group_index, group_length = group_position
    if group_length not in (4, 5, 6, 7):
        raise ValueError("Can only split groups of length 4, 5, 6, or 7 into one single and one group")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 1, min(group_length - 3, 3))

def split_group_into_two_identical_groups(group_position: GroupPosition, sticks: Sticks) -> Move:
    log('Split group into two identical groups')
    group_index, group_length = group_position
    if group_length not in (5, 6, 7, 8):
        raise ValueError("Can only split groups of length 5, 6, 7, or 8 into two identical groups")
    group_start = get_start_of_group(sticks, group_index)
    if group_length in (5, 6):
        return (group_start + 2, group_length - 4)
    elif group_length in (7, 8):
        return (group_start + 3, group_length - 6)

def split_group_into_two_different_groups(group_position: GroupPosition, sticks: Sticks) -> Move:
    log('Split group into two different groups')
    group_index, group_length = group_position
    if group_length not in (6, 7, 8):
        raise ValueError("Can only split groups of length 6, 7, or 8 into two different groups")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 2, group_length - 5)

# def leave_two_identical_groups(groups: Groups, sticks: Sticks) -> Move:
