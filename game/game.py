from game.config import LOG_ACTIVE
from game_types.game_types import Groups, Sticks, Move
import sys

def display_sticks(sticks: Sticks) -> None:
    stick_line = ''.join('|  ' if stick else '   ' for stick in sticks)
    number_line = ''.join(f"{str(i+1):<3}" if stick else '   ' for i, stick in enumerate(sticks))
    print(f"\n{stick_line}\n{number_line}")

def is_game_over(sticks: Sticks) -> bool:
    return sticks.count(True) == 0

def is_valid_move(sticks: Sticks, move: Move) -> bool:
    start, count = move
    if count not in [1, 2, 3]:
        print("You can only take 1, 2, or 3 sticks.")
        return False
    if start < 0 or start + count > len(sticks):
        print("Invalid stick positions.")
        return False
    if not all(sticks[start:start+count]):
        print("Those sticks are not all available.")
        return False
    return True

def remove_sticks(sticks: Sticks, move: Move) -> None:
    start, count = move
    for i in range(start, start+count):
        sticks[i] = False

def log(message: str, level = 'thinking'):
    if LOG_ACTIVE:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        CYAN = "\033[36m"
        RED = "\033[31m"
        ORANGE = "\033[38;5;208m"
        BG_BLACK = "\033[40m"
        WHITE = "\033[97m"

        if level == 'thinking':
            formatted_message = f"{BOLD}{CYAN}[THINKING] {message}{RESET}"
        elif level == 'info':
            formatted_message = f"{BOLD}{RED}  [INFO] {message}{RESET}"
        elif level == 'warn':
            formatted_message = f"{BOLD}{ORANGE}[WARN] {message}{RESET}"
        print(formatted_message, file=sys.stderr)

def create_sticks_from_groups(groups: Groups) -> Sticks:
    sticks: Sticks = []
    for group in groups:
        sticks += [True] * group
        sticks.append(False)
    return sticks