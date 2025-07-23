from game.game import is_valid_move, remove_sticks
from game_types.game_types import Sticks, Move

def get_player_move() -> Move:
    raw: str = input("Your move: ")
    start_str, count_str = raw.strip().split()
    start: int = int(start_str) - 1
    count: int = int(count_str)
    return start, count

def player_move(sticks: Sticks) -> None:
    while True:
        try:
            move = get_player_move()
            if not is_valid_move(sticks, move):
                continue
            remove_sticks(sticks, move)
            break
        except Exception:
            print("Invalid input. Please enter the start position and the number of sticks to take, e.g. 5 2.")