import numpy as np
import pygame
import sys
from game import BoardGame

W, H = 700, 800 
TOP_BAR_H  = 80
MARGIN     = 20

BOARD_X = MARGIN
BOARD_Y = TOP_BAR_H + MARGIN
BOARD_W = W - 2 * MARGIN          # 660
BOARD_H = H - TOP_BAR_H - 2 * MARGIN  # 680

BOARD_SIZE = 10
WIN_LENGTH  = 5
CELL_SIZE = BOARD_W // BOARD_SIZE


class TicTacToe(BoardGame):

    def reset(self):
        self.board          = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = 1
        self.winner         = None
        self.move_count     = 0
        self.winner_line = None

    def get_cell(self, x, y):
        c = (x - BOARD_X) // CELL_SIZE
        r = (y - BOARD_Y) // CELL_SIZE

        if 0 <= r <BOARD_SIZE and 0 <= c < BOARD_SIZE:
            return ((r, c))   
        else: return ((-1, -1))

    def check_win(self):
        rows = np.arange(BOARD_SIZE)[:,None,None]                 # (n,1,1)
        start_cols = np.arange(BOARD_SIZE-WIN_LENGTH+1)[None,:,None]  # (1,n-5+1,1)
        offsets = np.arange(WIN_LENGTH)[None,None,:]     # (1,1,5)

        row_windows = self.board[rows, start_cols+offsets]    # (n, n-5+1, 5)

        if(np.any(np.all(row_windows == self.current_player, axis = 2))):
            self.winner = self.current_player
            matches = np.argwhere(np.all(row_windows == self.current_player, axis = 2))
            for (x,y) in matches:
                self.winner_line = (y, x, 0)
                break
            return

        start_rows = np.arange(BOARD_SIZE-WIN_LENGTH+1)[:,None,None]  # (n-5+1,1,1)
        cols = np.arange(BOARD_SIZE)[None,:,None]                     # (1,n,1)
        offsets = np.arange(WIN_LENGTH)[None,None,:]         # (1,1,5)

        col_windows = self.board[start_rows+offsets, cols]        # (n-5+1, n, 5)
        if(np.any(np.all(col_windows == self.current_player, axis = 2))):
            self.winner = self.current_player
            matches = np.argwhere(np.all(col_windows == self.current_player, axis = 2))
            for (x,y) in matches:
                self.winner_line = (y, x, 90)
                break
            return
        
        start_rows = np.arange(BOARD_SIZE-WIN_LENGTH+1)[:,None,None]  # (n-5+1,1,1)
        start_cols = np.arange(BOARD_SIZE-WIN_LENGTH+1)[None,:,None]  # (1,n-5+1,1)
        offsets = np.arange(WIN_LENGTH)[None,None,:]         # (1,1,5)

        diag_windows = self.board[start_rows+offsets, start_cols+offsets]  # (n-5+1, n-5+1, 5)

        if(np.any(np.all(diag_windows == self.current_player, axis = 2))):
            self.winner = self.current_player
            matches = np.argwhere(np.all(diag_windows == self.current_player, axis = 2))
            for (x,y) in matches:
                self.winner_line = (y, x, 45)
                break
            return
        

        start_rows = np.arange(BOARD_SIZE-WIN_LENGTH+1)[:,None,None]   # (n-5+1,1,1)
        start_cols = np.arange(WIN_LENGTH-1, BOARD_SIZE)[None,:,None]  # (1,n-5+1,1)
        offsets = np.arange(WIN_LENGTH)[None,None,:]          # (1,1,5)

        anti_windows = self.board[start_rows+offsets, start_cols-offsets]  # (n-5+1, n-5+1, 5)


        if(np.any(np.all(anti_windows == self.current_player, axis = 2))):
            self.winner = self.current_player
            matches = np.argwhere(np.all(anti_windows== self.current_player, axis = 2))
            for (x,y) in matches:
                actual_col = y + (WIN_LENGTH - 1)
                self.winner_line = (actual_col , x, -45)
                break
            return
        
        if( self.move_count == BOARD_SIZE*BOARD_SIZE ):
            self.winner = 0


# ===========================================================================
    def draw_board(self, surf: pygame.Surface):
        pygame.draw.rect(surf, "yellow", (BOARD_X, BOARD_Y, CELL_SIZE*BOARD_SIZE, CELL_SIZE*BOARD_SIZE))

        # Draw grid
        for i in range(11):
            pygame.draw.line(surf, "black", (BOARD_X, BOARD_Y + i*CELL_SIZE), (BOARD_X + BOARD_W, BOARD_Y + i*CELL_SIZE), 3)
        for i in range(11):
            pygame.draw.line(surf, "black", (BOARD_X + i*CELL_SIZE, BOARD_Y ), (BOARD_X + i*CELL_SIZE, BOARD_Y + BOARD_W), 3)    

        self.draw_hovered_cell(surf)
        self.fill_board(surf)
        self.draw_top_bar(surf)

    def draw_top_bar(self, surf):
        pygame.draw.rect(surf, ( 18,  18,  35), (0, 0, W, TOP_BAR_H))
        game_text = self.get_font(35).render(self.__class__.__name__, True, "gold")
        surf.blit(game_text, (20,20))

        if( self.winner is None):
            p1_text = self.get_font(30).render(self.player_names[1], True, (255, 49, 49))
            p2_text = self.get_font(30).render(self.player_names[2], True, ( 60, 255, 255))
            vs_text = self.get_font(30).render(" vs ", True, (120, 120, 150))

            x = W / 2 - (p1_text.get_width() + p2_text.get_width() + vs_text.get_width()) / 2

            surf.blit(p1_text, (x, 20)); x += p1_text.get_width();
            surf.blit(vs_text, (x, 20)); x += vs_text.get_width();
            surf.blit(p2_text, (x, 20))

            turn_color = (255, 49, 49) if self.current_player == 1 else ( 90, 180, 255)
            turn_text = self.get_font(30).render(f"{self.current_player_name()}'s Turn", True, turn_color)
            surf.blit(turn_text, (W - turn_text.get_width() - 10, 20))

        elif self.winner == 0:
                draw_text = self.get_font(40).render("It's a Draw", True, "white")
                x = W / 2 - draw_text.get_width() / 2
                surf.blit(draw_text, (x, 20))

        else :
                winner_text = self.get_font(40).render(f"{self.player_names[self.winner]} Wins", True, "white")
                x = W / 2 - winner_text.get_width() / 2
                surf.blit(winner_text, (x, 20))
   
        pygame.draw.line (surf, ( 45,  45,  75), (0,TOP_BAR_H), (W, TOP_BAR_H))

    def fill_board(self, surf):
        centre=(CELL_SIZE//2, CELL_SIZE//2)
        for r,c in np.argwhere(self.board == 1) :
            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.line(surf, "red", (cx - CELL_SIZE/2*0.7, cy - CELL_SIZE/2*0.7),
                            (cx + CELL_SIZE/2*0.7, cy + CELL_SIZE/2*0.7), 5)
            pygame.draw.line(surf, "red", (cx - CELL_SIZE/2*0.7, cy + CELL_SIZE/2*0.7), 
                            (cx + CELL_SIZE/2*0.7, cy - CELL_SIZE/2*0.7), 5)
            
        for r,c in np.argwhere(self.board == 2) :
            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(surf, ( 60, 255, 255), (cx, cy), CELL_SIZE/2*0.9, 5)

    def draw_hovered_cell(self, surf:pygame.Surface):
        x, y = pygame.mouse.get_pos()
        c = (x - BOARD_X) // CELL_SIZE
        r = (y - BOARD_Y) // CELL_SIZE

        if 0 <= r <BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r,c] == 0:
            pygame.draw.rect(surf, (201, 197, 20), (BOARD_X + c*CELL_SIZE, BOARD_Y + r*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_line(self, screen, x, y, theta):
        cx = BOARD_X + CELL_SIZE*x + CELL_SIZE//2
        cy = BOARD_Y + CELL_SIZE*y + CELL_SIZE//2
        length = (WIN_LENGTH - 1)*CELL_SIZE

        if theta == 0:      # horizontal
            cx_f = cx + length
            cy_f = cy


        elif theta == 90:   # vertical
            cx_f = cx
            cy_f = cy + length
        elif theta == 45:   # main diagonal 
            cx_f = cx + length
            cy_f = cy + length
        elif theta == -45:  # anti-diagonal 
            cx_f = cx - length
            cy_f = cy + length


        pygame.draw.line(screen, "black", (cx, cy), (cx_f, cy_f), 5)


# ===========================================================================
    def handle_click(self, pos: tuple):
        x, y = pos
        r, c = self.get_cell(x, y)
        if ( r == -1 ): return
        if ( self.board[r, c] == 0):
            self.board[r, c] = self.current_player
            self.move_count += 1
            self.check_win()
            self.switch_turn()
# ===========================================================================
    def run_game(self,screen):
        running = True
        while  running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT ):
                    pygame.quit()
                    sys.exit(0)      

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

                screen.fill("red" if self.current_player == 1 else "blue")
                self.draw_board(screen)

                if self.winner == 1 or self.winner == 2:
                    self.draw_line(screen, *self.winner_line)

                if (self.winner != None):
                    pygame.display.update()
                    pygame.time.wait(1000)
                    if(self.winner == 0):
                        return None, None
                    else :
                        return self.player_names[self.winner], self.player_names[3 - self.winner]

                pygame.display.update()  
    
