from anbot.think.think_singles import get_groups_without_pairs_of_singles
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

def is_two_groups_and_one_single(groups: Groups) -> bool:
    if len(groups) != 3:
        return False
    return sum(1 for group in groups if group == 1) == 1