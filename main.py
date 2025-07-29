from game.game import display_sticks, is_game_over
from anbot.anbot import anbot_move  
from player.player import player_move
from game_types.game_types import Sticks

def main() -> None:
    print("\nWelcome to Sixteen Sticks! You are playing against an-bot. Don't take the last stick!")
    sticks: Sticks = [True] * 16
    player_turn: bool = True
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
