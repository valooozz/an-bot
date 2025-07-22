from typing import List, Tuple
from game import is_valid_move, remove_sticks

def get_player_move() -> Tuple[int, int]:
    raw: str = input("Your move: ")
    start_str, count_str = raw.strip().split()
    start: int = int(start_str) - 1
    count: int = int(count_str)
    return start, count

def player_move(sticks: List[bool]) -> None:
    while True:
        try:
            start, count = get_player_move()
            if not is_valid_move(sticks, start, count):
                continue
            remove_sticks(sticks, start, count)
            break
        except Exception:
            print("Invalid input. Please enter the start position and the number of sticks to take, e.g. 5 2.")