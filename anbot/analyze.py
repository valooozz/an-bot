from typing import List

from _pytest.stash import T
from anbot.think import get_groups_without_pairs_of_singles
from game.game import log
from game_types.game_types import Sticks, Groups

def analyze_sticks(sticks: Sticks) -> Groups:
    groups: Groups = []
    count = 0
    for stick in sticks:
        if stick:
            count += 1
        else:
            if count > 0:
                groups.append(count)
                count = 0
    if count > 0:
        groups.append(count)
    return groups

def is_only_singles_left(groups: Groups) -> bool:
    return all(group == 1 for group in groups)

def is_parity_state(groups: Groups) -> bool:
    count_big = 0
    for group in groups:
        if group in (2, 3, 4, 5):
            count_big += 1
        elif group != 1:
            return False
    return count_big == 1

def is_parity_even(groups: Groups) -> bool:
    return len(groups) % 2 == 0

def is_two_identical_groups_and_one_other(groups: Groups) -> bool:
    if len(groups) != 3:
        return False
    numbers_of_groups: List[int] = [0] * 4
    for group in groups:
        if group in (2, 3, 4, 5):
            numbers_of_groups[group - 2] += 1
    if any(count >= 2 for count in numbers_of_groups):
        return True
    return False

def is_one_little_group_and_one_big_group(groups: Groups) -> bool:
    if len(groups) != 2:
        return False
    little_group, big_group = sorted(groups)
    difference = big_group - little_group
    if little_group in (2, 3, 4, 5) and difference <= 3 and difference > 0:
        return True
    return False

def is_even_number_of_singles(groups: Groups) -> bool:
    number_of_singles = sum(1 for group in groups if group == 1)
    return number_of_singles > 0 and number_of_singles % 2 == 0
    
def is_almost_two_identical_groups(groups: Groups) -> bool:
    groups_without_pairs_of_singles, _ = get_groups_without_pairs_of_singles(groups)
    number_of_groups = len(groups_without_pairs_of_singles)
    if number_of_groups == 2:
        return is_one_little_group_and_one_big_group(groups_without_pairs_of_singles)    
    if number_of_groups == 3:
        return is_two_identical_groups_and_one_other(groups_without_pairs_of_singles)
    return False

def is_one_group_left(groups: Groups) -> bool:
    groups_without_pairs_of_singles, _ = get_groups_without_pairs_of_singles(groups)
    return len(groups_without_pairs_of_singles) == 1

def is_one_huge_group_and_one_other_group(groups: Groups) -> bool:
    if len(groups) != 2:
        return False
    big_group = sorted(groups)[1]
    if big_group >= 8:
        return True
    return False