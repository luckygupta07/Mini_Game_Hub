import pygame

def run_game(screen):

    board = [["" for _ in range(5)] for _ in range(5)]

    WIDTH, HEIGHT = screen.get_size()

   
    BG_COLOR   = (15, 15, 25)
    LINE_COLOR = (80, 80, 120)
    X_COLOR    = (220, 80, 80)
    O_COLOR    = (80, 180, 220)
    TEXT_COLOR = (200, 200, 220)
    BTN_COLOR  = (40, 40, 60)
    BTN_HOVER  = (60, 60, 90)

    
    GRID_SIZE   = min(WIDTH, HEIGHT) * 0.7
    CELL_SIZE   = GRID_SIZE // 5
    OFFSET_X    = (WIDTH  - GRID_SIZE) // 2
    OFFSET_Y    = (HEIGHT - GRID_SIZE) // 2 - 30
    LINE_WIDTH  = 4
    PIECE_WIDTH = 5

    font_big   = pygame.font.SysFont("Consolas", 42, bold=True)
    font_small = pygame.font.SysFont("Consolas", 24)

   
    screen.fill(BG_COLOR)

    
    for i in range(1, 5):
        x = int(OFFSET_X + i * CELL_SIZE)
        pygame.draw.line(screen, LINE_COLOR,
                         (x, int(OFFSET_Y)),
                         (x, int(OFFSET_Y + GRID_SIZE)), LINE_WIDTH)
        y = int(OFFSET_Y + i * CELL_SIZE)
        pygame.draw.line(screen, LINE_COLOR,
                         (int(OFFSET_X), y),
                         (int(OFFSET_X + GRID_SIZE), y), LINE_WIDTH)

    
    for row in range(5):
        for col in range(5):
            cx = int(OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2)
            cy = int(OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2)
            r  = int(CELL_SIZE * 0.3)

            if board[row][col] == "X":
                pygame.draw.line(screen, X_COLOR,
                                 (cx - r, cy - r), (cx + r, cy + r), PIECE_WIDTH)
                pygame.draw.line(screen, X_COLOR,
                                 (cx + r, cy - r), (cx - r, cy + r), PIECE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, O_COLOR, (cx, cy), r, PIECE_WIDTH)

    txt = font_big.render("Player X's turn", True, TEXT_COLOR)
    screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, int(OFFSET_Y - 60)))

   
    btn_rect = pygame.Rect(WIDTH // 2 - 80, int(OFFSET_Y + GRID_SIZE + 20), 160, 44)
    mouse    = pygame.mouse.get_pos()
    color    = BTN_HOVER if btn_rect.collidepoint(mouse) else BTN_COLOR
    pygame.draw.rect(screen, color, btn_rect, border_radius=8)
    btn_txt = font_small.render("Restart", True, TEXT_COLOR)
    screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                           btn_rect.centery - btn_txt.get_height() // 2))

    pygame.display.flip()
