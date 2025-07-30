from game_types.game_types import Groups


def is_parity_even(groups: Groups) -> bool:
    return len(groups) % 2 == 0