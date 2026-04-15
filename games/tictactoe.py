import numpy as np
import pygame
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

    def get_valid_moves(self) -> list:
        pass

    def make_move(self, move) -> bool:
        pass

    def check_winner(self):
        pass

    def draw_board(self, surf: pygame.Surface):
        pass

    def draw_top_bar(self, surf):
        pygame.draw.rect(surf, ( 18,  18,  35), (0, 0, W, TOP_BAR_H))
        game_text = self.get_font(30, True).render(self.__class__.__name__, True, (120, 120, 150))
        surf.blit(game_text, (20,20))

        p1_text = self.get_font(30).render(self.player_names[0], True, (255,  90,  90))
        p2_text = self.get_font(30).render(self.player_names[1], True, ( 90, 180, 255))
        vs_text = self.get_font(30).render(" VS ", True, (120, 120, 150))

        x = W / 2 - (p1_text.get_width() + p2_text.get_width() + vs_text.get_width()) / 2

        surf.blit(p1_text, (x, 20)); x += p1_text.get_width();
        surf.blit(vs_text, (x, 20)); x += vs_text.get_width();
        surf.blit(p2_text, (x, 20))

        turn_color = (255,  90,  90) if self.current_player == 1 else ( 90, 180, 255)
        turn_text = self.get_font(30).render(self.current_player_name(), True, turn_color)
        surf.blit(turn_text, (W - turn_text.get_width() - 10, 20))

        pygame.draw.line (surf, ( 45,  45,  75), (0,TOP_BAR_H), (W, TOP_BAR_H))

    def handle_click(self, pos: tuple):
        pass
        
