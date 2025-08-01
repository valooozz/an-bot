from game.config import INITIAL_POSITION, NUMBER_OF_STICKS, SANDBOX_ACTIVE
from game.game import create_sticks_from_groups, display_sticks, is_game_over
from anbot.anbot import anbot_move  
from player.player import player_move
from game_types.game_types import Sticks

def main() -> None:
    print("\nWelcome to The Sticks Game! You are playing against an-bot. Don't take the last stick!")
    if (SANDBOX_ACTIVE):
        sticks = create_sticks_from_groups(INITIAL_POSITION)
        player_turn = False
    else:
        sticks: Sticks = [True] * NUMBER_OF_STICKS
        player_turn = True
    while True:
        display_sticks(sticks)
        if is_game_over(sticks):
            if player_turn:
                print("An-bot took the last stick. You win!")
            else:
                print("You took the last stick. You lose!")
            break
        if player_turn:
            player_move(sticks)
        else:
            anbot_move(sticks)
        player_turn = not player_turn

if __name__ == "__main__":
    main()
