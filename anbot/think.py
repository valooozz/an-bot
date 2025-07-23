from game_types.game_types import Sticks


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