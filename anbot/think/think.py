from typing import Tuple
from game.config import NUMBER_OF_STICKS
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
    smallest_group = (0, NUMBER_OF_STICKS)
    for idx, group in enumerate(groups):
        if group < 2:
            continue
        if group > biggest_group[1]:
            biggest_group = (idx, group)
        if group < smallest_group[1]:
            smallest_group = (idx, group)
    return (biggest_group, smallest_group)

def get_the_little_group(groups: Groups) -> GroupPosition:
    sorted_groups = sorted(groups)
    little_group = None
    for i in range(3):
        first = i
        second = (i + 1) % 3
        third = (i + 2) % 3
        if sorted_groups[first] in (2, 3, 4) and sorted_groups[third] == sorted_groups[second] + 1 :
            little_group = sorted_groups[first]
            break
    for idx, group in enumerate(groups):
        if group == little_group:
            return (idx, little_group)