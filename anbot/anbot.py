from typing import List
from anbot.analyze.analyze import analyze_sticks, is_one_group_left, is_one_huge_group_and_one_other_group, is_only_singles_left, is_two_close_groups_and_one_little_group, is_two_groups_and_one_single
from anbot.analyze.analyze_parity import is_parity_even, is_parity_state
from anbot.analyze.analyze_identical import is_almost_two_identical_groups
from anbot.score.score import get_best_move_by_score
from anbot.think.think_singles import add_indexes_of_removed_singles, get_groups_without_pairs_of_singles
from anbot.think.think import get_biggest_and_smallest_groups, get_huge_group, get_the_little_group
from anbot.think.think_parity import get_group_in_parity_state
from game.config import ANBOT_MODE
from game.game import is_valid_move, log, remove_sticks
from game_types.game_types import Groups, Sticks, Move
from anbot.do.do import leave_one_single_from_group, leave_two_identical_groups, reduce_group, take_first_single, take_whole_group
from anbot.do.do_split import split_group_by_taking_one_stick, split_group_into_one_single_and_one_group, split_group_into_two_identical_groups, split_group_into_two_singles, split_huge_group_into_two_different_groups
from game.game import log
import random

def get_valid_moves(sticks: Sticks) -> List[Move]:
    # Returns a list of (start, count) tuples for valid moves
    moves: List[Move] = []
    n: int = len(sticks)
    i: int = 0
    while i < n:
        if sticks[i]:
            for count in range(1, 4):
                if i + count <= n and all(sticks[i:i+count]):
                    moves.append((i, count))
            # Skip to next untaken stick
            while i < n and sticks[i]:
                i += 1
        else:
            i += 1
    return moves

def handle_parity(sticks: Sticks, groups: Groups) -> Move:
    group_to_take = get_group_in_parity_state(groups)
    group_length = group_to_take[1]
    log(f"Group in parity state: {group_to_take}")

    if is_parity_even(groups):
        log('Even parity')
        if group_length in (4, 5):
            move = split_group_into_two_singles(group_to_take, sticks)
        else:
            move = take_whole_group(group_to_take, sticks)
    
    else: # odd parity
        log('Odd parity')
        if group_length == 5:
            move = split_group_into_two_identical_groups(group_to_take, sticks)
        else:
            move = leave_one_single_from_group(group_to_take, sticks)
    
    return move

def handle_one_group(sticks: Sticks, groups: Groups) -> Move:
    groups_without_pairs_of_singles, indexes_of_removed_singles = get_groups_without_pairs_of_singles(groups)
    group_length = groups_without_pairs_of_singles[0]
    log(f"Last group of {group_length}")
    real_group_index = add_indexes_of_removed_singles(0, indexes_of_removed_singles)
    group_left = (real_group_index, group_length)
    number_of_sticks_to_take = (group_length - 1) % 4

    if number_of_sticks_to_take == 0:
        return split_group_by_taking_one_stick(0, sticks)

    return reduce_group(group_left, group_length - number_of_sticks_to_take, sticks)

def handle_two_groups_and_one_single(sticks: Sticks, groups: Groups) -> Move:
    big_group, small_group = get_biggest_and_smallest_groups(groups)
    size_of_small_group = small_group[1]
    move = split_group_into_one_single_and_one_group(big_group, size_of_small_group, sticks)
    if move:
        return move
    return reduce_group(big_group, size_of_small_group + 1, sticks)

def handle_two_close_groups_and_one_little_group(sticks: Sticks, groups: Groups) -> Move:
    little_group = get_the_little_group(groups)
    return reduce_group(little_group, 1, sticks)

def handle_huge_group(sticks: Sticks, groups: Groups) -> Move:
    group_position = get_huge_group(groups)
    return split_huge_group_into_two_different_groups(group_position, sticks)

def print_move(move: Move):
    start, count = move
    print(f"\nAn-bot takes {count} stick{count > 1 and 's' or ''} starting at position {start+1}.")

def print_invalid_move(move: Move):
    start, count = move
    log(f"An-bot tried to do an invalid move : {count} stick{count > 1 and 's' or ''} starting at position {start+1}.", 'warn')

def apply_move(sticks: Sticks, move: Move):
    print_move(move)
    remove_sticks(sticks, move)

def try_move(sticks: Sticks, move: Move) -> bool:
    if move:
        if is_valid_move(sticks, move):
            apply_move(sticks, move)
            return True
        else:
            print_invalid_move(move)
    return False

def anbot_move(sticks: Sticks) -> None:
    if ANBOT_MODE == 'SCORING':
        move = get_best_move_by_score(sticks)
        if try_move(sticks, move): return

    groups = analyze_sticks(sticks)
    move: Move = None

    if is_only_singles_left(groups):
        log('Only singles left')
        move = take_first_single(sticks)
        if try_move(sticks, move): return

    if is_one_group_left(groups):
        log('One group left')
        move = handle_one_group(sticks, groups)
        if try_move(sticks, move): return

    if is_parity_state(groups):
        log('In parity state')
        move = handle_parity(sticks, groups)
        if try_move(sticks, move): return

    if is_almost_two_identical_groups(groups):
        log('Almost two identical groups')
        move = leave_two_identical_groups(groups, sticks)
        if try_move(sticks, move): return

    if is_two_groups_and_one_single(groups):
        log('Two groups and one single')
        move = handle_two_groups_and_one_single(sticks, groups)
        if try_move(sticks, move): return
    
    if is_two_close_groups_and_one_little_group(groups):
        log('Two close groups and one little group')
        move = handle_two_close_groups_and_one_little_group(sticks, groups)
        if try_move(sticks, move): return

    if ANBOT_MODE == 'HYBRID':
        move = get_best_move_by_score(sticks)
        if try_move(sticks, move): return
        
    if is_one_huge_group_and_one_other_group(groups):
        log('One huge group and one other group')
        move = handle_huge_group(sticks, groups)
        if try_move(sticks, move): return
    
    # Simple AI: random valid move
    log('Random move')
    moves: List[Move] = get_valid_moves(sticks)
    move: Move = random.choice(moves)
    apply_move(sticks, move)