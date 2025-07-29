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
        if group in (2, 3, 4):
            count_big += 1
        elif group != 1:
            return False
    return count_big == 1

def is_parity_even(groups: Groups) -> bool:
    return len(groups) % 2 == 0