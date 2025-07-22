from typing import List, Tuple
import random

def get_valid_moves(sticks: List[bool]) -> List[Tuple[int, int]]:
    # Returns a list of (start, count) tuples for valid moves
    moves: List[Tuple[int, int]] = []
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

def anbot_move(sticks: List[bool]) -> None:
    moves: List[Tuple[int, int]] = get_valid_moves(sticks)
    # Simple AI: random valid move
    move: Tuple[int, int] = random.choice(moves)
    start, count = move
    print(f"\nAn-bot takes {count} stick{count > 1 and 's' or ''} starting at position {start+1}.")
    for i in range(start, start+count):
        sticks[i] = False