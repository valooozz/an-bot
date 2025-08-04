from typing import Tuple
from game_types.game_types import Groups, Indexes


def get_number_of_singles(groups: Groups) -> Groups:
    return sum(1 for group in groups if group == 1)

def remove_singles(groups: Groups, accept_one: bool) -> Groups:
    new_groups: Groups = []
    for group in groups:
        if group == 1 and accept_one:
            new_groups.append(1)
            accept_one = False
        elif group != 1:
            new_groups.append(group)
    return new_groups

def get_groups_without_pairs_of_singles(groups: Groups) -> Groups:
    number_of_singles = get_number_of_singles(groups)
    is_odd = number_of_singles % 2 != 0
    return remove_singles(groups, is_odd)