from game_types.game_types import Groups


def is_parity_state(groups: Groups) -> bool:
    count_big = 0
    for group in groups:
        if group in (2, 3, 4, 5):
            count_big += 1
        elif group != 1:
            return False
    return count_big == 1

def is_parity_even(groups: Groups) -> bool:
    return len(groups) % 2 == 0
