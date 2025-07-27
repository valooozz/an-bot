from anbot.analyze import is_parity_even
from game_types.game_types import Sticks, Groups, Move
from typing import Tuple

def get_start_of_group(sticks: Sticks, index_of_group: int) -> int:
    group_count = 0
    in_group = False
    for i, stick in enumerate(sticks):
        if stick:
            if not in_group:
                if group_count == index_of_group:
                    return i
                group_count += 1
                in_group = True
        else:
            in_group = False
    raise ValueError("Group index out of range")

def get_group_in_parity_state(groups: Groups) -> Tuple[int, int]:
    for idx, group in enumerate(groups):
        if group != 1:
            return idx, group


# def get_move_when_parity(sticks: Sticks, groups: Groups) -> Move:
#     if is_parity_even(groups):
#         # Find the index and value of the group that is not 1 (there is only one such group)
        
#         if group in [2, 3]:
#             return get_start_of_group(sticks, )