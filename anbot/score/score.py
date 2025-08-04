import random
from statistics import mean
from typing import Dict, List
from anbot.analyze.analyze import analyze_sticks, is_exact_groups, is_only_singles_left
from anbot.analyze.analyze_identical import is_n_identical_groups
from anbot.analyze.analyze_parity import is_parity_state
from anbot.think.think_singles import get_groups_without_pairs_of_singles
from game.config import DIGGING_LEVEL
from game.game import log
from game_types.game_types import Groups, Move, Sticks

def get_possible_moves(sticks: Sticks) -> List[Move]:
    possible_moves: List[Move] = []
    for i in range(len(sticks)):
        current_stick = sticks[i]
        next_stick = False
        next_next_stick = False
        if (i + 1 < len(sticks)):
            next_stick = sticks[i + 1]
            if (i + 2 < len(sticks)):
                next_next_stick = sticks[i + 2]
        if current_stick:
            possible_moves.append((i, 1))
            if next_stick:
                possible_moves.append((i, 2))
                if next_next_stick:
                    possible_moves.append((i, 3))
    return possible_moves

def simulate_remove_sticks(sticks: Sticks, move: Move) -> Sticks:
    start, count = move
    number_of_sticks = len(sticks)
    next_position = [False] * number_of_sticks
    for i in range(number_of_sticks):
        if not(start <= i < start + count):
            next_position[i] = sticks[i]
    return next_position

def assign_simple_score(groups: Groups) -> int:
    if groups == []:
        return -1
    if groups == [1]:
        return 1
    if is_only_singles_left(groups):
        return 1 if len(groups) % 2 == 0 else -1
    if is_parity_state(groups):
        return -1
    if is_n_identical_groups(groups, 2) and groups[0] in (2, 3, 4, 5):
        return 1
    if is_n_identical_groups(groups, 4) and groups[0] in (2, 3):
        return 1
    if len(groups) == 1 and groups[0] in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
        return -1
    if is_exact_groups(groups, [1, 2, 3]):
        return 1
    if is_exact_groups(groups, [2, 3, 4]):
        return -1
    if is_exact_groups(groups, [2, 2, 3, 3]):
        return 1
    return 0

def assign_score_by_digging(sticks: Sticks, level: int) -> int:
    if level > DIGGING_LEVEL:
        return 0
    possible_moves = get_possible_moves(sticks)
    scores = get_scores(possible_moves, sticks, level + 1)
    mean_score = sum(scores.values()) / len(scores)
    if level % 2 == 0: # an-bot turn
        return max(scores.values()) * mean_score * -1
    else: # player turn
        return min(scores.values()) * mean_score

def assign_score_to_move(move: Move, sticks: Sticks, level: int) -> int:
    next_position = simulate_remove_sticks(sticks, move)
    next_groups = analyze_sticks(next_position)
    next_groups_without_singles, _ = get_groups_without_pairs_of_singles(next_groups)
    score = assign_simple_score(next_groups_without_singles)
    if score == 0:
        score = assign_score_by_digging(next_position, level)
    return score

def get_scores(possible_moves: List[Move], sticks: Sticks, level: int) -> Dict[Move, int]:
    dict_of_scores: Dict[Move, int] = {}
    for possible_move in possible_moves:
        dict_of_scores[possible_move] = assign_score_to_move(possible_move, sticks, level)
    return dict_of_scores

def get_move_with_best_score(scores: Dict[Move, int]) -> Move:
    max_score = max(scores.values())
    log(f"Score of chosen move : {max_score}")
    best_moves = [move for move, score in scores.items() if score == max_score]
    return random.choice(best_moves)

def get_best_move_by_score(sticks: Sticks) -> Move:
    possible_moves = get_possible_moves(sticks)
    scores = get_scores(possible_moves, sticks, 1)
    log(f"Scores : {scores}")
    return get_move_with_best_score(scores)