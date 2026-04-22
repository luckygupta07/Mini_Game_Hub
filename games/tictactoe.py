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

    def __init__(self, player1, player2):
        super.__init__(player1, player2)


    def get_cell(self, x, y):
        c = (x - BOARD_X) // CELL_SIZE
        r = (y - BOARD_Y) // CELL_SIZE

        if 0 <= r <BOARD_SIZE and 0 <= c < BOARD_SIZE:
            return ((r, c))   
        else: return ((-1, -1))

    def check_win(self):
        from numpy.lib.stride_tricks import sliding_window_view

        rows = sliding_window_view(self.board, (1, WIN_LENGTH)).reshape(-1, WIN_LENGTH)
        if(np.any(np.all(rows == self.current_player, axis = 1))):
            self.winner = self.current_player
            return

        cols = sliding_window_view(self.board, (WIN_LENGTH, 1)).reshape(-1, WIN_LENGTH)
        if(np.any(np.all(cols == self.current_player, axis = 1))):
            self.winner = self.current_player
            return
        
        diags = sliding_window_view(self.board, (WIN_LENGTH, WIN_LENGTH)).reshape(-1, WIN_LENGTH, WIN_LENGTH)
        diags = diags[:, range(WIN_LENGTH), range(WIN_LENGTH)]
        if(np.any(np.all(diags == self.current_player, axis = 1))):
            self.winner = self.current_player
            return
        
        anti_diags = sliding_window_view(self.board, (WIN_LENGTH, WIN_LENGTH)).reshape(-1, WIN_LENGTH, WIN_LENGTH)
        anti_diags = anti_diags[:, range(WIN_LENGTH),range(WIN_LENGTH-1, -1, -1)]
        if(np.any(np.all(anti_diags == self.current_player, axis = 1))):
            self.winner = self.current_player
            return
        
        if( self.move_count == BOARD_SIZE*BOARD_SIZE ):
            self.winner = 0

# ===========================================================================
    def draw_board(self, surf: pygame.Surface):
        # Draw grid
        for i in range(11):
            pygame.draw.line(surf, "white", (BOARD_X, BOARD_Y + i*CELL_SIZE), (BOARD_X + BOARD_W, BOARD_Y + i*CELL_SIZE))
        for i in range(11):
            pygame.draw.line(surf, "white", (BOARD_X + i*CELL_SIZE, BOARD_Y ), (BOARD_X + i*CELL_SIZE, BOARD_Y + BOARD_W))    

        self.fill_board(surf)
        self.draw_top_bar(surf)

    def draw_top_bar(self, surf):
        pygame.draw.rect(surf, ( 18,  18,  35), (0, 0, W, TOP_BAR_H))
        game_text = self.get_font(30, True).render(self.__class__.__name__, True, (120, 120, 150))
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


# ===========================================================================
    def handle_click(self, pos: tuple):
        x, y = pos
        r, c = self.get_cell(x, y)
        if ( r == -1 ): return
        if ( self.board[r, c] == 0):
            self.board[r, c] = self.current_player
            self.check_win()
            self.move_count += 1
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

                screen.fill("black")
                self.draw_board(screen)
                if (self.winner != None):
                    pygame.display.update()
                    pygame.time.wait(1000)
                    if(self.winner == 0):
                        return None, None
                    else :
                        return self.player_names[self.winner], self.player_names[3 - self.winner]

                pygame.display.update()  
    
