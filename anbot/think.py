from game_types.game_types import GroupPosition, Sticks, Groups
from typing import Tuple

def get_index_of_first_single(sticks: Sticks) -> int:
    for i, stick in enumerate(sticks):
        if stick:
            left_empty = (i == 0 or not sticks[i - 1])
            right_empty = (i == len(sticks) - 1 or not sticks[i + 1])
            if left_empty and right_empty:
                return i
    raise ValueError("No single stick found")

def get_start_of_group(sticks: Sticks, index_of_group: int) -> int:
    group_count = 0
    in_group = False
    for i, stick in enumerate(sticks):
        if stick:
            if not in_group:
                if group_count == index_of_group:
                    return i
                group_count += 1
                in_group = True
        else:
            in_group = False
    raise ValueError("Group index out of range")

def get_group_in_parity_state(groups: Groups) -> GroupPosition:
    for idx, group in enumerate(groups):
        if group != 1:
            return idx, group

def get_group_different_from_the_others(groups: Groups) -> GroupPosition:
    if len(groups) != 3:
        raise ValueError("Not exactly three groups")
    a, b, c = groups
    if a == b == c:
        return 0, a
    if a == b:
        return 2, c
    if a == c:
        return 1, b
    # b == c
    return 0, a

def get_biggest_group_between_two(groups: Groups) -> Tuple[GroupPosition, int]:
    if len(groups) != 2:
        raise ValueError("There must be exactly two groups")
    if groups[0] == groups[1]:
        raise ValueError("The two groups must be different")
    if groups[0] >= groups[1]:
        return (0, groups[0]), groups[1]
    else:
        return (1, groups[1]), groups[0]


def remove_singles(groups: Groups) -> Groups:
    return [group for group in groups if group != 1]