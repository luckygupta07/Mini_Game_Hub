import sys
import os
import csv
import subprocess
import pygame
import numpy as np
from datetime import date


GAME_MODULES = {
    "Tic-Tac-Toe": ("games.tictactoe",  "TicTacToe"),
    "Othello":      ("games.othello",   "Othello"),
    "Connect Four": ("games.connect4",  "ConnectFour"),
}

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
    # Window & layout constants
    W, H = 700, 800 

    TOP_BAR_H  = 80
    MARGIN     = 20

    BOARD_X = MARGIN
    BOARD_Y = TOP_BAR_H + MARGIN
    BOARD_W = W - 2 * MARGIN          # 660
    BOARD_H = H - TOP_BAR_H - 2 * MARGIN  # 680

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

    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:  ####
        return pygame.font.SysFont("segoeui", size, bold=bold)

    def draw_something(self,surf: pygame.Surface):
        
        pass


# ===========================================================================
# Menu screen
# ===========================================================================
class MenuScreen:

    GAMES = list(GAME_MODULES.keys())

    DESCRIPTIONS = {
        "Tic-Tac-Toe": "10 × 10  ·  5 in a row to win",
        "Othello":      "8 × 8   ·  Flip your opponent's discs",
        "Connect Four": "7 × 7   ·  Drop balls, connect 4",
    }

    def __init__(self, screen: pygame.Surface, p1: str, p2: str):
        self.screen = screen
        self.p1     = p1
        self.p2     = p2

        self.row_h    = 100
        self.row_left  = 80
        self.row_w    = W - 160
        first_row_y   = 320
        self.row_tops = [first_row_y + i * (self.row_h + 16) for i in range(len(self.GAMES))]

        #Font styles
        self.f_title = pygame.font.SysFont("segoeui", 60, bold=True)
        self.f_sub   = pygame.font.SysFont("segoeui", 50)
        self.f_game  = pygame.font.SysFont("segoeui", 30, bold=True) ####
        self.f_hint  = pygame.font.SysFont("segoeui", 15)

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
        return pygame.Rect(self.row_left, self.row_tops[idx], self.row_w, self.row_h)

    def row_num(self, mx: int, my: int) -> int:
        for i in range(len(self.GAMES)):
            if self.row_rect(i).collidepoint(mx, my):
                return i
        return -1

    def draw_something(self, mx: int, my: int):
        surf = self.screen
        surf.fill((10,10,20))

        #Title
        title = self.f_title.render("MINI  GAME  HUB", True, (220, 220, 235))
        surf.blit(title, (W // 2 - title.get_width() // 2, 80))

        p1s = self.f_sub.render(self.p1, True, (255, 90, 90))
        vs = self.f_sub.render("  vs  ", True, (110, 110, 140))
        p2s = self.f_sub.render(self.p2, True, (90, 180, 255))
        total = p1s.get_width() + vs.get_width() + p2s.get_width()
        x = W//2 - total // 2
        y = 150
        surf.blit(p1s, (x, y)); x += p1s.get_width()
        surf.blit(vs, (x, y)); x += vs.get_width()
        surf.blit(p2s, (x, y))

        pygame.draw.line(surf, (45, 45, 75),
                         (W // 2 - 150, 210), (W // 2 + 150, 210), 1)

        sel_label = self.f_hint.render("Select a game to play", True, (90, 90, 120))
        surf.blit(sel_label, (W // 2 - sel_label.get_width() // 2, 220))

        # Game rows
        hov = self.row_num(mx, my)
        for i, name in enumerate(self.GAMES):
            r      = self.row_rect(i)
            is_hov = (i == hov)
            bg_col = (28, 28, 50) if is_hov else (16, 16, 30)
            pygame.draw.rect(surf, bg_col, r, border_radius=8)
            if is_hov:
                pygame.draw.rect(surf, (80, 180, 255),
                                 (r.x, r.y + 10, 3, r.height - 20),
                                 border_radius=2)
            name_col = (220, 220, 235) if is_hov else (160, 160, 185)
            surf.blit(self.f_game.render(name, True, name_col),
                      (r.x + 20, r.y + 14))
            surf.blit(self.f_hint.render(self.DESCRIPTIONS[name], True, (90, 90, 120)),
                      (r.x + 20, r.y + 44))
            if i < len(self.GAMES) - 1:
                sep_y = r.bottom + 7
                pygame.draw.line(surf, (28, 28, 48),
                                 (r.x, sep_y), (r.x + r.w, sep_y), 1)


def load_game_class(game_name: str):
    """Dynamically import and return the game class for the selected game.
        Prevents circular import error.
    """
    import importlib
    module_path, class_name = GAME_MODULES[game_name]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)




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