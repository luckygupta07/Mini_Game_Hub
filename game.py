import sys
import os
import csv
import subprocess
import pygame
from datetime import date

from games.tictactoe import TicTacToe
from games.connect4 import ConnectFour
from games.othello import Othello


# Paths
# ---------------------------------------------------------------------------
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
HISTORY_CSV     = os.path.join(BASE_DIR, "history.csv")
LEADERBOARD_SH  = os.path.join(BASE_DIR, "leaderboard.sh")
# ---------------------------------------------------------------------------


# Visual constants
# ---------------------------------------------------------------------------

# window size
W, H = 900, 700          

# Colours 
C = {
    
}

GAME_ICONS = {
    "Tic-Tac-Toe": "✕  ○",
    "Othello":     "●  ○",
    "Connect Four":"⬡  ⬡",
}
# ---------------------------------------------------------------------------


# Appends game result to history.csv
# ---------------------------------------------------------------------------
def record_result(winner_name: str, loser_name: str, game_name: str):
    with open(HISTORY_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([winner_name, loser_name, date.today().isoformat(), game_name])
# ---------------------------------------------------------------------------


def load_game_class(game_name: str):
    """Return the game class based on the given name (brute force style)."""
    if game_name == "TicTacToe":
        return TicTacToe
    elif game_name == "ConnectFour":
        return ConnectFour
    elif game_name == "Othello":
        return Othello

def main():
    # Validate arguments
    if len(sys.argv) != 3:
        print("Usage: python3 game.py <username1> <username2>")
        sys.exit(1)

    p1, p2 = sys.argv[1], sys.argv[2]

    # Initialise Pygame
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Mini Game Hub")


    # Hub loop
    running = True
    while running:
       pass

    pygame.quit()


if __name__ == "__main__":
    main()
