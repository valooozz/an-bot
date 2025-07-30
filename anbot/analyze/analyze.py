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
    
def is_parity_state(groups: Groups) -> bool:
    count_big = 0
    for group in groups:
        if group in (2, 3, 4, 5):
            count_big += 1
        elif group != 1:
            return False
    return count_big == 1

def is_one_huge_group_and_one_other_group(groups: Groups) -> bool:
    if len(groups) != 2:
        return False
    big_group = sorted(groups)[1]
    if big_group >= 8:
        return True
    return False