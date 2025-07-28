from anbot.think import get_start_of_group
from game_types.game_types import GroupPosition, Move, Sticks

def take_whole_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    group_index, group_length = group_position
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length)

def split_group_into_two_singles(group_position: GroupPosition, sticks: Sticks) -> Move:
    group_index, group_length = group_position
    if group_length not in (3, 4, 5):
        raise ValueError("Can only split groups of length 3, 4, or 5 into two singles")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 1, group_length - 2)

def leave_one_single_from_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    group_index, group_length = group_position
    if group_length not in (2, 3, 4):
        raise ValueError("Can only leave one single from groups of length 2, 3, or 4")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length - 1)