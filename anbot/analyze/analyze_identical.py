from typing import List
from anbot.think.think_singles import get_groups_without_pairs_of_singles
from game_types.game_types import Groups


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
    
def is_almost_two_identical_groups(groups: Groups) -> bool:
    groups_without_pairs_of_singles, _ = get_groups_without_pairs_of_singles(groups)
    number_of_groups = len(groups_without_pairs_of_singles)
    if number_of_groups == 2:
        return is_one_little_group_and_one_big_group(groups_without_pairs_of_singles)    
    if number_of_groups == 3:
        return is_two_identical_groups_and_one_other(groups_without_pairs_of_singles)
    return False