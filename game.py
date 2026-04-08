import sys
import os
import csv
import subprocess
import pygame
import numpy as np
from datetime import date

from games.tictactoe import TicTacToe
from games.connect4 import ConnectFour
from games.othello import Othello


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
HISTORY_CSV     = os.path.join(BASE_DIR, "history.csv")
LEADERBOARD_SH  = os.path.join(BASE_DIR, "leaderboard.sh")

# ---------------------------------------------------------------------------
# Visual constants
# ---------------------------------------------------------------------------

# window size
W, H = 700, 800          

# Colours 
C = {
    
}

GAME_CLASSES = {
    "Tic-Tac-Toe": TicTacToe,
    "Othello": Othello,
    "Connect Four": ConnectFour
}

# ---------------------------------------------------------------------------
# Appends game result to history.csv
# ---------------------------------------------------------------------------
def record_result(winner_name: str, loser_name: str, game_name: str):
    with open(HISTORY_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([winner_name, loser_name, date.today().isoformat(), game_name])
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
#Base class for 2-player turn-based board games
# ---------------------------------------------------------------------------
class BoardGame:
    #Base class for 2-player turn-based board games rendered in Pygame.
    def __init__(self, player1: str, player2: str):
        self.player_names   = {1: player1, 2: player2}
        self.current_player = 1
        self.board: np.ndarray = None
        self.winner         = None
        self.move_count     = 0
        self.reset()

    def switch_turn(self):
        self.current_player = 2 if self.current_player == 1 else 1

    def is_game_over(self) -> bool:
        return self.winner is not None

    def current_player_name(self) -> str:
        return self.player_names[self.current_player]

    def opponent_player(self) -> int:
        return 2 if self.current_player == 1 else 1

    def get_result_string(self) -> str:
        if self.winner == 0:
            return "It's a draw!"
        return f"{self.player_names[self.winner]} wins!"

    def draw_something(self,surf: pygame.Surface):
        pass


# ===========================================================================
# Menu screen
# ===========================================================================
class MenuScreen:

    GAMES = list(GAME_CLASSES.keys())

    DESCRIPTIONS = {
        "Tic-Tac-Toe": "10 × 10  ·  5 in a row to win",
        "Othello":      "8 × 8   ·  Flip your opponent's discs",
        "Connect Four": "7 × 7   ·  Drop balls, connect 4",
    }

    def __init__(self, screen: pygame.Surface, p1: str, p2: str):
        self.screen = screen
        self.p1     = p1
        self.p2     = p2

        self.row_h    = 72
        self.row_bod    = 80
        self.row_w    = W - 160
        first_row_y   = 260
        self.row_tops = [first_row_y + i * (self.row_h + 16) for i in range(len(self.GAMES))]

    def run(self) -> str:
        clock = pygame.time.Clock()
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    idx = self.row_num(mx, my)
                    if idx >= 0:
                        return self.GAMES[idx]
            self.draw_something(mx, my)
            pygame.display.flip()
            clock.tick(60)

    def row_rect(self, idx: int) -> pygame.Rect:
        return pygame.Rect(self.row_x, self.row_tops[idx], self.row_w, self.row_h)

    def row_num(self, mx: int, my: int) -> int:
        for i in range(len(self.GAMES)):
            if self.row_rect(i).collidepoint(mx, my):
                return i
        return -1

    def draw_something(self, mx: int, my: int):
        pass


# ===========================================================================
# Main Function
# ===========================================================================
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
    while True:
        menu      = MenuScreen(screen, p1, p2)
        game_name = menu.run()

        if game_name is None:
            break



    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()