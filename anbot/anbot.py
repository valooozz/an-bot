from typing import List
from anbot.analyze import analyze_sticks, is_parity_even, is_parity_state
from anbot.do import leave_one_single_from_group, split_group_into_two_singles, take_whole_group
from anbot.think import get_group_in_parity_state
from game.game import is_valid_move, remove_sticks
from game_types.game_types import Sticks, Groups, Move
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

    if is_parity_even(groups):
        if group_to_take[0] in (4, 5):
            move = split_group_into_two_singles(group_to_take, sticks)
        else:
            move = take_whole_group(group_to_take, sticks)
    
    else: # odd parity
        move = leave_one_single_from_group(group_to_take, sticks)
    
    return move

def print_move(move: Move):
    count, start = move
    print(f"\nAn-bot takes {count} stick{count > 1 and 's' or ''} starting at position {start+1}.")

def print_invalid_move(move: Move):
    count, start = move
    print(f"\nAn-bot tried to do an invalid move : {count} stick{count > 1 and 's' or ''} starting at position {start+1}.")

def apply_move(sticks: Sticks, move: Move):
    print_move(move)
    remove_sticks(sticks, move)

def anbot_move(sticks: Sticks) -> None:
    groups = analyze_sticks(sticks)
    move: Move | None = None

    if is_parity_state(groups):
        move = handle_parity(sticks, groups)

    if move:
        if is_valid_move(sticks, move):
            apply_move(sticks, move)
        else:
            print_invalid_move(move)

    # Simple AI: random valid move
    moves: List[Move] = get_valid_moves(sticks)
    move: Move = random.choice(moves)
    apply_move(sticks, move)