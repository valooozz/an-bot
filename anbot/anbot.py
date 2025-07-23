from typing import List
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

def anbot_move(sticks: Sticks) -> None:
    moves: List[Move] = get_valid_moves(sticks)
    # Simple AI: random valid move
    move: Move = random.choice(moves)
    start, count = move
    print(f"\nAn-bot takes {count} stick{count > 1 and 's' or ''} starting at position {start+1}.")
    for i in range(start, start+count):
        sticks[i] = False

def analyze_sticks(sticks: Sticks) -> Groups:
    groups: Groups = []
    count = 0
    for stick in sticks:
        if stick:
            count += 1
        else:
            if count > 0:
                groups.append(count)
                count = 0
    if count > 0:
        groups.append(count)
    return groups

def only_singles_left(groups: Groups) -> bool:
    return all(group == 1 for group in groups)