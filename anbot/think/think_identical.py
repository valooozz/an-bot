from typing import Tuple
from game_types.game_types import GroupPosition, Groups


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