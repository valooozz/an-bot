from typing import List

def display_sticks(sticks: List[bool]) -> None:
    stick_line = ''.join('|  ' if stick else '   ' for stick in sticks)
    number_line = ''.join(f"{str(i+1):<3}" if stick else '   ' for i, stick in enumerate(sticks))
    print(f"\n{stick_line}\n{number_line}")

def is_game_over(sticks: List[bool]) -> bool:
    return sticks.count(True) == 0

def is_valid_move(sticks: List[bool], start: int, count: int) -> bool:
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

def remove_sticks(sticks: List[bool], start: int, count: int) -> None:
    for i in range(start, start+count):
        sticks[i] = False