from typing import List
from anbot.cache import write_best_moves
from anbot.scoring import get_best_move_by_score
from game.game import is_valid_move, log, remove_sticks
from game_types.game_types import Sticks, Move
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
    move = get_best_move_by_score(sticks)
    if try_move(sticks, move): return
    
    log('Random move')
    moves: List[Move] = get_valid_moves(sticks)
    move: Move = random.choice(moves)
    apply_move(sticks, move)