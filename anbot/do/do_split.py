from ctypes import sizeof
from anbot.think.think import get_start_of_group
from game.game import log
from game_types.game_types import GroupPosition, Move, Sticks


def split_group_into_two_singles(group_position: GroupPosition, sticks: Sticks) -> Move:
    log(f"Split group into two singles : {group_position}")
    group_index, group_length = group_position
    if group_length not in (3, 4, 5):
        raise ValueError("Can only split groups of length 3, 4, or 5 into two singles")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 1, group_length - 2)

def split_group_into_one_single_and_one_group(group_position: GroupPosition, size_of_new_group: int, sticks: Sticks) -> Move:
    log(f"Split group into one single and one group of {size_of_new_group} : {group_position}")
    group_index, group_length = group_position
    if group_length not in (4, 5, 6, 7):
        raise ValueError("Can only split groups of length 4, 5, 6, or 7 into one single and one group")
    if group_length - size_of_new_group < 2:
        log(f"Tried to split group of {group_length} into a single and a group of {size_of_new_group} : not enough sticks", 'warn')
        return None
    number_of_sticks_to_remove = group_length - size_of_new_group - 1
    if number_of_sticks_to_remove > 3:
        log(f"Tried to split group of {group_length} into a single and a group of {size_of_new_group} : too many sticks to remove", 'warn')
        return None
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 1, number_of_sticks_to_remove)

def split_group_by_taking_one_stick(group_index: int, sticks: Sticks) -> Move:
    log(f"Split group by taking one stick : {group_index}")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 1, 1)

def split_group_into_two_identical_groups(group_position: GroupPosition, sticks: Sticks) -> Move:
    log(f"Split group into two identical groups : {group_position}")
    group_index, group_length = group_position
    if group_length not in (5, 6, 7, 8, 9, 10, 11, 12, 13):
        raise ValueError("Can only split groups of length 5, 6, 7, 8, 9, 10, 11, 12 or 13 into two identical groups")
    group_start = get_start_of_group(sticks, group_index)
    shift = max(group_length // 2 - 1, 2)
    return (group_start + shift, group_length - shift * 2)

def split_group_into_two_different_groups(group_position: GroupPosition, sticks: Sticks) -> Move:
    log(f"Split group into two different groups : {group_position}")
    group_index, group_length = group_position
    if group_length not in (6, 7, 8):
        raise ValueError("Can only split groups of length 6, 7, or 8 into two different groups")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + 2, group_length - 5)

def split_huge_group_into_two_different_groups(group_position: GroupPosition, sticks: Sticks) -> Move:
    log(f"Split huge group into two different groups: {group_position}")
    group_index, group_length = group_position
    if group_length < 8:
        raise ValueError("Can only split huge groups of length higher or equals to 8 into two different groups")
    group_start = get_start_of_group(sticks, group_index)
    return (group_start + (group_length - 8) // 3 + 3, group_length - (group_length - 8) // 3 * 3 - 7)