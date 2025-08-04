from game.config import INITIAL_POSITION, NUMBER_OF_STICKS, PLAYER_ACTIVE, PLAYER_TURN, SANDBOX_ACTIVE
from game.game import create_sticks_from_groups, display_sticks, is_game_over
from anbot.anbot import anbot_move  
from player.player import player_move
from game_types.game_types import Sticks

def main() -> None:
    print("\nWelcome to The Sticks Game! You are playing against an-bot. Don't take the last stick!")
    player_turn = PLAYER_TURN
    if (SANDBOX_ACTIVE):
        sticks = create_sticks_from_groups(INITIAL_POSITION)
    else:
        sticks: Sticks = [True] * NUMBER_OF_STICKS
    while True:
        display_sticks(sticks)
        if is_game_over(sticks):
            if player_turn:
                print("An-bot took the last stick. You win!")
            else:
                print("You took the last stick. You lose!")
            break
        if player_turn and PLAYER_ACTIVE:
            player_move(sticks)
        else:
            anbot_move(sticks)
        player_turn = not player_turn

if __name__ == "__main__":
    main()
