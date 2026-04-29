import sys
import os
import csv
import subprocess
import pygame

import numpy as np

from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


GAME_MODULES = {
    "Tic-Tac-Toe": ("games.tictactoe",  "TicTacToe"),
    "Othello":      ("games.othello",   "Othello"),
    "ConnectFour": ("games.connect4",  "ConnectFour"),
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
def show_leaderboard(sort_by):
    #sort_by can be 'wins', 'losses', or 'ratio'.
    subprocess.run(["bash", LEADERBOARD_SH, sort_by])


#--gamefrequency updating------------------------------------------------------
def update_game_frequency(game_name: str):
    with open("games_frequency.csv", "r") as f:
        values = f.readline().strip("\n").split(",")
    
    n1, n2, n3 = int(values[0]), int(values[1]), int(values[2])

    if game_name == "ConnectFour":
        n1 += 1
    elif game_name == "Othello":
        n2 += 1
    elif game_name == "Tic-Tac-Toe":
        n3 += 1

    with open("games_frequency.csv", "w") as f:
        f.write(f"{n1},{n2},{n3}\n")


#----------------------------------------------------------------------------
#showing statitics
#----------------------------------------------------------------------------
def show_statitics(screen:pygame.Surface):
    top_5_users=[]
    users_wins=[]
    users_loses=[]
    with open('count_of_games.csv','r') as f:
        for i in range(0,5):
            k=f.readline().strip("\n").split(",")
            top_5_users.append(k[0])
            users_wins.append(int(k[1]))
            users_loses.append(int(k[5]))
    x=np.arange(len(top_5_users))
    #-------creating a required layout--------------------
    fig=plt.figure(figsize=(W/100,H/100),dpi=100)
    gs=fig.add_gridspec(2,2,height_ratios=[1,1])

    bar=fig.add_subplot(gs[0,:])
    pie1=fig.add_subplot(gs[1,0])
    pie2=fig.add_subplot(gs[1,1])
    
    #---------drawing bar graph----------------------------
    
    b1=bar.bar(x,users_wins,0.3,label="Total no of wins",color="blue")
    bar.bar_label(b1,users_wins,padding=0.10)
    b2=bar.bar(x + 0.3,users_loses,0.3,label="Total no of loses",color="red")
    bar.bar_label(b2,users_loses,padding=0.10)
    bar.set_xticks(x+0.15,top_5_users)
    bar.set_xlabel("Top 5 players")
    bar.set_ylabel("Frequency")
    bar.set_title("total no of games won by top 5 players")
    bar.legend()

    
    #---------drawing piecharts-----------------------------
    
    #Piechart 1 -----------------------------
    labels=['connect4','othello','tictactoe']
    with open('games_frequency.csv','r') as f:
        frequency=f.readline().strip("\n").split(",")
    pie1.pie(frequency,labels=None,autopct='%1.1f%%',startangle=30)
    pie1.legend(labels=labels)
    pie1.set_title("GAME POPULARITY")
    pie1.set_frame_on(True)

    #Piechart 2-----------------------------
    with open('count_of_games.csv','r') as f:
        wins=f.readline().strip("\n").split(",")[2:5]
    pie2.pie(wins,labels=None,autopct='%1.1f%%',startangle=30)
    pie2.legend(labels=labels)
    pie2.set_title("wins contribution for top player")
    pie2.set_frame_on(True)

    plt.tight_layout()
    
    plt.savefig('images/statistics.png', dpi=100, pad_inches=0)
    plt.close()


    text=pygame.font.Font(None,40)
    text_s=text.render("Press 'SPACE' to CONTINUE",1,"black")
    text_r=text_s.get_rect()
    text_r.midbottom=(W/2,H)


    a=True
    while a:
        image_s=pygame.image.load("images/statistics.png")
        image_s = pygame.transform.scale(image_s, (W, H))
        screen.blit(image_s,(0,0))
        screen.blit(text_s,text_r)
        pygame.display.update()
        for e in pygame.event.get():
            if(e.type==pygame.QUIT):
                pygame.quit()
                sys.exit()
            if(e.type == pygame.KEYDOWN):
                if(e.key == pygame.K_SPACE):
                    a=False
    os.remove('count_of_games.csv')


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

    def get_font(self, size: int, bold: bool=False) -> pygame.font.Font:  ####
        return pygame.font.SysFont("segoeui", size, bold)


# ===========================================================================
# Menu screen
# ===========================================================================
class MenuScreen:

    GAMES = list(GAME_MODULES.keys())

    DESCRIPTIONS = {
        "Tic-Tac-Toe": "10 × 10  ·  5 in a row to win",
        "Othello":      "8 × 8   ·  Flip your opponent's discs",
        "ConnectFour": "7 × 7   ·  Drop balls, connect 4",
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

        
        #Images 
        self.bg_image = pygame.image.load("images/menu.png")   # replace with your file path
        self.bg_image = pygame.transform.scale(self.bg_image, (W, H))

        self.c4_image = pygame.image.load("images/c4.png")
        self.c4_image = pygame.transform.smoothscale(self.c4_image, (self.row_h, self.row_h))

        self.tic_image = pygame.image.load("images/tic.png")
        self.tic_image = pygame.transform.smoothscale(self.tic_image, (self.row_h, self.row_h))

        self.ot_image = pygame.image.load("images/ot.png")
        self.ot_image = pygame.transform.smoothscale(self.ot_image, (self.row_h, self.row_h))



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
    
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:  ####
        return pygame.font.SysFont("segoeui", size, bold)

    def draw_something(self, mx: int, my: int):
        surf = self.screen
        
        surf.blit(self.bg_image, (0, 0))

        p1s = self.get_font(50).render(self.p1, True, (255, 90, 90))
        vs = self.get_font(50).render("  vs  ", True, (110, 110, 140))
        p2s = self.get_font(50).render(self.p2, True, (90, 180, 255))
        total = p1s.get_width() + vs.get_width() + p2s.get_width()
        x = W//2 - total // 2
        y = 160
        surf.blit(p1s, (x, y)); x += p1s.get_width()
        surf.blit(vs, (x, y)); x += vs.get_width()
        surf.blit(p2s, (x, y))

        pygame.draw.line(surf, (45, 45, 75),
                         (W // 2 - 150, 210), (W // 2 + 150, 210), 1)

        sel_label = self.get_font(15).render("Select a game to play", True, (90, 90, 120))
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
            surf.blit(self.get_font(30).render(name, True, name_col),
                      (r.x + 20 + self.row_h, r.y + 20))
            surf.blit(self.get_font(15).render(self.DESCRIPTIONS[name], True, (90, 90, 120)),
                      (r.x + 20 + self.row_h, r.y + 50))
            
            if i == 0:
                surf.blit(self.tic_image, (self.row_left, self.row_tops[i]))

            elif i == 1:
                surf.blit(self.ot_image, (self.row_left, self.row_tops[i]))

            elif i == 2:
                surf.blit(self.c4_image, (self.row_left, self.row_tops[i]))
                
            if i < len(self.GAMES) - 1:
                sep_y = r.bottom + 7
                pygame.draw.line(surf, (28, 28, 48),
                                 (r.x, sep_y), (r.x + r.w, sep_y), 1)

# ===========================================================================
# Post-game screen
# ===========================================================================
class Postgame:

    SORT_OPTIONS = ["wins", "losses", "ratio"]
    SORT_LABELS = {
        "wins":   "Sort by Wins",
        "losses": "Sort by Losses",
        "ratio":  "Sort by W/L Ratio",
    }

    def __init__(self,screen,result_str, winner, loser, game_name):
        self.screen = screen
        self.result_str = result_str
        self.winner = winner
        self.loser = loser
        self.game_name = game_name

        self.phase = "sort"
        #Variables for sort option buttons
        self.btn_w, self.btn_h = 200, 46
        self.gap = 20
        total = len(self.SORT_OPTIONS) * self.btn_w + (len(self.SORT_OPTIONS) - 1) * self.gap
        self.start_x = W // 2 - total // 2
        self.btn_y = H // 2 + 60
        self.btn_x = [self.start_x + i*(self.btn_w+self.gap) for i in range(len(self.SORT_OPTIONS))]

        self.bg_image = pygame.image.load("images/post_game.png")   # replace with your file path
        self.bg_image = pygame.transform.scale(self.bg_image, (W, H))
    

    def run(self):
        clock = pygame.time.Clock()
        while True:
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if self.phase == "again":
                        if event.key == pygame.K_y:
                            return True
                        if event.key in (pygame.K_n, pygame.K_ESCAPE):
                            return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.phase == "sort":
                        idx = self.handle_sort_click(mx, my)
                        if idx >=0 :
                            self.handle_sort_chosen(idx)
                    
                    elif self.phase == "again":
                        pick = self.handle_again(mx, my)
                        if pick == "Yes":
                            return True
                        elif pick == "No":
                            return False

            self.draw_bg(self.screen)
            pygame.display.update()
            clock.tick(60)



    def sort_options_rect(self, idx):
        return pygame.Rect(self.btn_x[idx], self.btn_y, self.btn_w, self.btn_h)
    
    def play_again_rect(self):
        return pygame.Rect(W // 2 - 215, H // 2 + 60, 190, 50)
     
    def quit_rect(self):
        return pygame.Rect(W // 2 + 25, H // 2 + 60, 190, 50)

    def handle_sort_click(self, mx, my):
        for i in range (len(self.SORT_OPTIONS)):
            if self.sort_options_rect(i).collidepoint(mx, my):
                return i
        return -1
        
    def handle_sort_chosen(self, idx):
        if self.winner is not None:
            record_result(self.winner,self.loser, self.game_name)
        else:
            print("\nGame ended in a draw — no result recorded.\n")

        show_leaderboard(self.SORT_OPTIONS[idx])
        self.phase = "statistics"

    def handle_again(self, mx, my):
        if self.play_again_rect().collidepoint(mx, my):
            return "Yes"
        elif self.quit_rect().collidepoint(mx, my):
            return "No"
        else :
            return None
        
    def get_font(self, size: int, bold: bool = False) -> pygame.font.Font:  ####
        return pygame.font.SysFont("segoeui", size, bold=bold)


    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
  
    def draw_bg(self,surf: pygame.Surface):

        surf.blit(self.bg_image, (0, 0))

    # Central frame
        rect_w = 660
        rect_h = 320 if self.phase == "sort" else 260
        rect_x = W // 2 - rect_w // 2
        rect_y = H // 2 - rect_h // 2 
        pygame.draw.rect(surf, ( 28,  28,  50),
                         (rect_x, rect_y, rect_w, rect_h), border_radius=16)
        pygame.draw.rect(surf, ( 70,  70, 110),
                         (rect_x, rect_y, rect_w, rect_h), 1, border_radius=16)
        
        res = self.get_font(36, True).render(self.result_str, True, "gold")
        surf.blit(res, res.get_rect(center=(W // 2, rect_y + 58)))

        pygame.draw.line(surf, ( 70,  70, 110), (rect_x + 30,rect_y + 90), (rect_x + rect_w - 30, rect_y + 90),1)

        if self.phase == "sort":
            self.draw_sort_phase(surf, rect_y)
        elif self.phase == "statistics":
            show_statitics(self.screen)
            self.phase="again"
        else :
            self.draw_again_phase(surf, rect_y)

    def draw_sort_phase(self, surf: pygame.Surface, rect_y):
        options_text = self.get_font(21, True).render("Choose leaderboard sort metric:", True, "white")
        surf.blit(options_text, options_text.get_rect(center=(W // 2, rect_y +  120)))

        hint = self.get_font(15).render("Result will be saved and leaderboard printed in terminal", True, (110, 110, 140))
        surf.blit(hint, hint.get_rect(center=(W // 2, rect_y + 148)))

        for i in range(len(self.SORT_OPTIONS)):
            r = self.sort_options_rect(i)
            pygame.draw.rect(surf, ( 50,  50,  80), r, border_radius=10)
            pygame.draw.rect(surf, ( 70,  70, 110), r, 1, border_radius=10)

            label = self.get_font(16).render(self.SORT_LABELS[self.SORT_OPTIONS[i]], True, (160, 160, 185))
            surf.blit(label, label.get_rect(center=(r.centerx, r.centery)))

    def draw_again_phase(self, surf: pygame.Surface, rect_y):
        again_text = self.get_font(21).render("Play another game?", True, "white")
        surf.blit(again_text, again_text.get_rect(center = (W // 2, rect_y + 120)))

        hint = self.get_font(15).render(
        "Y  →  back to menu           N / Esc  →  quit", True, (110, 110, 140))
        surf.blit(hint, hint.get_rect(center = (W // 2, rect_y + 150)))

        for rect, label in [(self.play_again_rect(), "Play Again"), (self.quit_rect(), "Quit")]:
            pygame.draw.rect(surf, ( 50,  50,  80), rect, border_radius=10)
            pygame.draw.rect(surf, ( 70,  70, 110), rect, 1, border_radius=10)

            btn_label = self.get_font(16).render(label, True, (160, 160, 185))
            surf.blit(btn_label, btn_label.get_rect(center = (rect.centerx, rect.centery)))
                
        

def load_game_class(game_name: str):
    """Dynamically import and return the game class for the selected game.
        Prevents circular import error.
    """
    import importlib
    module_path, class_name = GAME_MODULES[game_name]
    module = importlib.import_module(module_path)
    return getattr(module, class_name)

def start_game(screen: pygame.Surface, game_name: str, p1: str, p2: str):

    GameClass = load_game_class(game_name)
    game      = GameClass(p1, p2)

    winner, loser = game.run_game(screen)
    return winner, loser



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
            # Window closed from menu
            break

        # Run selected game
        winner, loser = start_game(screen, game_name, p1, p2)
        update_game_frequency(game_name)
        

        result_str = f"{winner} wins!" if winner else "It's a draw!"
        post = Postgame(screen, result_str, winner, loser, game_name)
        play_again = post.run()

        if not play_again:
            break


    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
