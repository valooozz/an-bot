from anbot.think import get_start_of_group
from game_types.game_types import GroupPosition, Sticks

def take_whole_group(groupToTake: GroupPosition, sticks: Sticks):
    group_index, group_length = groupToTake
    group_start = get_start_of_group(sticks, group_index) 
    for j in range(group_start, group_start + group_length):
        sticks[j] = False

def split_group_into_two_singles(groupPosition: GroupPosition, sticks: Sticks):
    group_index, group_length = groupPosition
    if group_length not in (3, 4, 5):
        raise ValueError("Can only split groups of length 3, 4, or 5 into two singles")
    group_start = get_start_of_group(sticks, group_index)
    if group_length == 3:
        sticks[group_start + 1] = False
    elif group_length == 4:
        sticks[group_start + 1] = False
        sticks[group_start + 2] = False
    elif group_length == 5:
        sticks[group_start + 1] = False
        sticks[group_start + 2] = False
        sticks[group_start + 3] = False

def leave_one_single_from_group(groupPosition: GroupPosition, sticks: Sticks):
    group_index, group_length = groupPosition
    if group_length not in (2, 3, 4):
        raise ValueError("Can only leave one single from groups of length 2, 3, or 4")
    group_start = get_start_of_group(sticks, group_index)
    for j in range(group_start + 1, group_start + group_length):
        sticks[j] = False