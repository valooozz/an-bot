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

def is_exact_groups(groups: Groups, value: Groups) -> bool:
    return sorted(groups) == value

def is_n_identical_groups(groups: Groups, n: int) -> bool:
    if len(groups) != n:
        return False
    value = groups[0]
    for group in groups:
        if group != value:
            return False
    return True

def is_one_group_left(groups: Groups) -> bool:
    return len(groups) == 1