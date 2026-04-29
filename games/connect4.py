import numpy as np
import pygame
import sys
from game import BoardGame


W, H = 700, 800 
TOP_BAR_H  = 80
MARGIN     = 40

BOARD_SIZE = 7
WIN_LENGTH  = 4

CELL_SIZE =  88
BOARD_W = CELL_SIZE * BOARD_SIZE   # 616

BOARD_X = MARGIN
BOARD_Y = TOP_BAR_H + CELL_SIZE 
BOARD_H = BOARD_W  # 616


class ConnectFour(BoardGame):

    def reset(self):
        self.board          = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.current_player = 1
        self.winner         = None
        self.move_count     = 0
    
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
    # Draw

    def draw_board(self, surf: pygame.Surface):
        """Render full frame. Call self.draw_top_bar(surf) here."""
        
        pygame.draw.rect(surf, "blue", (BOARD_X, BOARD_Y , BOARD_W, BOARD_H ), border_radius=4)

        if self.winner is None:
            self.draw_hovered_column(surf)
            self.draw_floating_ball(surf)

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2

                pygame.draw.circle(surf, "black", (cx, cy), CELL_SIZE/2*0.9)


        self.fill_board(surf)
        self.draw_top_bar(surf)
    
    def draw_hovered_column(self, surf:pygame.Surface):
        x, y = pygame.mouse.get_pos()
        c = (x - BOARD_X) // CELL_SIZE
        r = (y - BOARD_Y) // CELL_SIZE

        if -1 <= r <BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[0,c] == 0:
            pygame.draw.rect(surf, (16, 83, 156), (BOARD_X + c*CELL_SIZE, BOARD_Y, CELL_SIZE, BOARD_H))

    def draw_floating_ball(self, surf:pygame.Surface):
        x, y = pygame.mouse.get_pos()
        c = (x - BOARD_X) // CELL_SIZE
        r = (y - BOARD_Y) // CELL_SIZE

        if -1 <= r <BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[0,c] == 0:
            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y - CELL_SIZE // 2 
            pygame.draw.circle(surf, "red" if self.current_player == 1 else ( 60, 255, 255), (cx, cy), CELL_SIZE/2*0.9)


    def draw_top_bar(self, surf):
            pygame.draw.rect(surf, ( 18,  18,  35), (0, 0, W, 80))
            game_text = self.get_font(30).render(self.__class__.__name__, True, "gold")
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

            pygame.draw.line (surf, ( 45, 45, 75), (0, 80), (W, 80))

    def fill_board(self, surf):
        centre=(CELL_SIZE//2, CELL_SIZE//2)
        for r,c in zip(*np.where(self.board==1)):
            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(surf, "red", (cx, cy), CELL_SIZE/2*0.9)
            
        for r,c in zip(*np.where(self.board==2)):
            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(surf, ( 60, 255, 255), (cx, cy), CELL_SIZE/2*0.9)

    def draw_line(self, screen, x, y, theta):
        cx = BOARD_X + CELL_SIZE*x + CELL_SIZE//2
        cy = BOARD_Y + CELL_SIZE*y + CELL_SIZE//2
        length = (WIN_LENGTH - 1)*CELL_SIZE

        if theta == 0:      # horizontal
            cx_f = cx + length
            cy_f = cy

            for i in range(WIN_LENGTH):
                pygame.draw.circle(screen, "gold", (cx + i*CELL_SIZE, cy), CELL_SIZE/2*0.9, 6)

        elif theta == 90:   # vertical
            cx_f = cx
            cy_f = cy + length

            for i in range(WIN_LENGTH):
                pygame.draw.circle(screen, "gold", (cx, cy + i*CELL_SIZE), CELL_SIZE/2*0.9, 6)

        elif theta == 45:   # main diagonal 
            cx_f = cx + length
            cy_f = cy + length

            for i in range(WIN_LENGTH):
                pygame.draw.circle(screen, "gold", (cx + i*CELL_SIZE, cy + i*CELL_SIZE), CELL_SIZE/2*0.9, 6)

        elif theta == -45:  # anti-diagonal 
            cx_f = cx - length
            cy_f = cy + length

            for i in range(WIN_LENGTH):
                pygame.draw.circle(screen, "gold", (cx - i*CELL_SIZE, cy + i*CELL_SIZE), CELL_SIZE/2*0.9, 6)

        pygame.draw.line(screen, "gold", (cx, cy), (cx_f, cy_f), 5)


# ===========================================================================
    #Mouse
    def handle_click(self, pos: tuple, surf:pygame.Surface):
        x, y = pos
        r, c = self.get_cell(x, y)

        if ( r == -1 or self.board[0,c] != 0 ): return

        clock     = pygame.time.Clock()

        for i in range(BOARD_SIZE):

            if self.board[i, c] !=0 :
                break

            cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y + i * CELL_SIZE + CELL_SIZE // 2

            # Redraw board otherwise whole path is colored
            self.draw_board(surf)
            # Draw ball at current falling position
            pygame.draw.circle(surf, (60,255,255) if self.current_player == 2 else "red", (cx, cy), CELL_SIZE//2*0.9)

            pygame.display.update()
            clock.tick(15) 

        for i in range(BOARD_SIZE-1, -1, -1):
            if self.board[i, c] == 0:
                self.board[i, c] = self.current_player
                self.check_win()
                self.move_count += 1
                self.switch_turn()
                break

# ===========================================================================
    def run_game(self,screen):
        running = True
        while  running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT ):
                    pygame.quit()
                    sys.exit(0)      

                if event.type == pygame.MOUSEMOTION:
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos(), screen)

                screen.fill("black")
                self.draw_board(screen)

                if self.winner is not None:
                    self.draw_line(screen, *self.winner_line)

                if (self.winner != None):
                    pygame.display.update()
                    pygame.time.wait(1000)
                    if(self.winner == 0):
                        return None, None
                    else :
                        return self.player_names[self.winner], self.player_names[3 - self.winner]

                pygame.display.update()
