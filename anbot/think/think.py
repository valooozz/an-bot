from typing import Tuple
from game_types.game_types import GroupPosition, Sticks, Groups


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

def get_huge_group(groups: Groups) -> GroupPosition:
    for idx, group in enumerate(groups):
        if group >= 8:
            return (idx, group)

def get_biggest_and_smallest_groups(groups: Groups) -> Tuple[GroupPosition, GroupPosition]:
    biggest_group = (0, 0)
    smallest_group = (0, 0)
    for idx, group in enumerate(groups):
        if group == 1:
            continue
        if group > biggest_group:
            biggest_group = (idx, group)
        elif group < smallest_group:
            smallest_group = (idx, group)
    return (biggest_group, smallest_group)