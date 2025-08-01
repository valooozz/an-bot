from anbot.think.think import get_index_of_first_single, get_start_of_group
from anbot.think.think_identical import get_biggest_group_between_two, get_group_different_from_the_others
from anbot.think.think_singles import add_indexes_of_removed_singles, get_groups_without_pairs_of_singles
from anbot.do.do_split import split_group_into_two_identical_groups, split_group_into_two_singles
from game.game import log
from game_types.game_types import GroupPosition, Groups, Move, Sticks

def take_first_single(sticks: Sticks) -> Move:
    log('Take first single')
    first_single_index = get_index_of_first_single(sticks)
    return (first_single_index, 1)

def take_whole_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    log(f"Take whole group : {group_position}")
    group_index, group_length = group_position
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length)

def reduce_group(group_position: GroupPosition, new_length: int, sticks: Sticks) -> Move:
    group_index, group_length = group_position
    log(f"Reduce group of {group_length} into group of {new_length}")
    if group_length <= new_length:
        log(f"Group length is lower or equal to the new length ({group_length} <= {new_length})", 'warn')
        return None
    if group_length - new_length > 3:
        log(f"Too many sticks to remove ({group_length} -> {new_length})", 'warn')
        return None
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length - new_length)

def leave_one_single_from_group(group_position: GroupPosition, sticks: Sticks) -> Move:
    log(f"Leave one single from group : {group_position}")
    group_index, group_length = group_position
    if group_length not in (2, 3, 4):
        raise ValueError("Can only leave one single from groups of length 2, 3, or 4")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start, group_length - 1)

def leave_two_identical_groups(groups: Groups, sticks: Sticks) -> Move:
    log('Leave two identical groups')
    groups_without_pairs_of_singles, indexes_of_removed_singles = get_groups_without_pairs_of_singles(groups)
    number_of_groups = len(groups_without_pairs_of_singles)
    if number_of_groups not in (2, 3):
        raise ValueError("There must be only two or three groups")
    if number_of_groups == 2:
        log('From two remaining groups')
        (group_index, group_length), new_length = get_biggest_group_between_two(groups_without_pairs_of_singles)
        real_group_index = add_indexes_of_removed_singles(group_index, indexes_of_removed_singles)
        return reduce_group((real_group_index, group_length), new_length, sticks)
    elif number_of_groups == 3:
        log('From three remaining groups')
        group_index, group_length = get_group_different_from_the_others(groups_without_pairs_of_singles)
        real_group_index = add_indexes_of_removed_singles(group_index, indexes_of_removed_singles)
        if group_length in (1, 2, 3):
            return take_whole_group((real_group_index, group_length), sticks)
        elif group_length in (4, 5):
            log('Leaving two singles')
            return split_group_into_two_singles((real_group_index, group_length), sticks)
        elif group_length in (6, 7, 8, 9, 10, 11, 12, 13):
            log('Leaving two identical groups')
            return split_group_into_two_identical_groups((real_group_index, group_length), sticks)