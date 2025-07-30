from typing import Tuple
from game_types.game_types import Groups, Indexes


def get_number_of_singles(groups: Groups) -> Groups:
    return sum(1 for group in groups if group == 1)

def remove_singles(groups: Groups, accept_one: bool) -> Tuple[Groups, Indexes]:
    new_groups: Groups = []
    indexes_of_removed_singles: Indexes = []
    for idx, group in enumerate(groups):
        if group == 1 and accept_one:
            new_groups.append(1)
            accept_one = False
        elif group != 1:
            new_groups.append(group)
        else:
            indexes_of_removed_singles.append(idx)
    return new_groups, indexes_of_removed_singles

def get_groups_without_pairs_of_singles(groups: Groups) -> Tuple[Groups, Indexes]:
    number_of_singles = get_number_of_singles(groups)
    is_odd = number_of_singles % 2 != 0
    return remove_singles(groups, is_odd)

def add_indexes_of_removed_singles(index: int, indexes_of_removed_singles: Indexes) -> int:
    real_index = index
    for index_removed in indexes_of_removed_singles:
        if index_removed <= real_index:
            real_index += 1
    return real_index