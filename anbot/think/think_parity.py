from game_types.game_types import GroupPosition, Groups


def get_group_in_parity_state(groups: Groups) -> GroupPosition:
    for idx, group in enumerate(groups):
        if group != 1:
            return idx, group