import pygame 
import sys
import numpy as np
from button import Button

pygame.init()

BG = pygame.Color("#203972")
BLUE = pygame.Color("#3E5AAA")
H_BLUE = pygame.Color("#6477AF")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FF7276")
H_RED = pygame.Color("#FFAAAC")
YELLOW = pygame.Color("#FFF36D")
H_YELLOW = pygame.Color("#EBE6B6")
WHITE = pygame.Color("#FFFFFF")

ROW_COUNT = 5
COLUMN_COUNT = 5
SQUARESIZE = 110
board_width = COLUMN_COUNT * SQUARESIZE
board_height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 40)

screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MINIMAX AI")

def create_board():
    board = [
        [0, 3, 0, 3, 0],
        [3, 0, 0, 0, 3],
        [0, 0, 3, 0, 0],
        [3, 0, 0, 0, 3],
        [0, 3, 0, 3, 0]
    ]

    return board

def print_board(board):
    print(board)

def draw_lines_between_zeros(board):
    width_center = (screen_width / 2) - (board_width / 2)
    zero_positions = [(r, c) for r in range(ROW_COUNT) for c in range(COLUMN_COUNT) if board[r][c] == 0]

    for pos1 in zero_positions:
        for pos2 in zero_positions:
            if pos1 != pos2:
                # Check if pos1 and pos2 are adjacent
                if abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1:
                    pygame.draw.line(screen, WHITE, (pos1[1] * SQUARESIZE + SQUARESIZE / 2 + width_center, board_height - pos1[0] * SQUARESIZE - SQUARESIZE / 2),
                                     (pos2[1] * SQUARESIZE + SQUARESIZE / 2 + width_center, board_height - pos2[0] * SQUARESIZE - SQUARESIZE / 2), 5)


def draw_board(board):
    width_center = (screen_width/2) - (board_width/2)
    # Board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != 3:
                pygame.draw.rect(screen, BLUE, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            else:
                pygame.draw.rect(screen, H_BLUE, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, board_height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 1: 
                pygame.draw.circle(screen, YELLOW, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, board_height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    draw_lines_between_zeros(board)
    pygame.display.update()

def six_men_morris():
    screen.fill(BLACK)
    playing = True
    board = create_board()
    print_board(board)
    draw_board(board)

    while playing:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=None, pos=(75,30), 
                            text_input="MENU", font=get_font(29, 1), base_color=WHITE, hovering_color=H_BLUE)
        RESET_BUTTON = Button(image=None, pos=(75, screen_height-30), 
                            text_input="RESET", font=get_font(29, 1), base_color=WHITE, hovering_color=H_BLUE)
        QUIT_BUTTON = Button(image=None, pos=(screen_width-75, screen_height-30), 
                            text_input="QUIT", font=get_font(29, 1), base_color=RED, hovering_color=H_RED)
        
        for button in [MENU_BUTTON, RESET_BUTTON, QUIT_BUTTON]:
            button.changeColor(GAME_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(GAME_MOUSE_POS):
                    main()
                if RESET_BUTTON.checkForInput(GAME_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(GAME_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()



# Frontend functions
def get_font(size, type):
    if type == 1:
        return pygame.font.SysFont("Franklin Gothic Heavy", size)
    else:
        return pygame.font.SysFont("Arial Narrow", size)

def main():
    running = True
    # background = pygame.image.load("GAME BG.png")
    while running:
        screen.fill(BG)
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=None, pos=(screen_width//4, 350), 
                            text_input="PLAY GAME", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        CONTROLS_BUTTON = Button(image=None, pos=(screen_width//4, 450), 
                            text_input="CONTROLS", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        QUIT_BUTTON = Button(image=None, pos=(screen_width//4, 550), 
                            text_input="QUIT GAME", font=get_font(68, 1), base_color="#D32735", hovering_color=RED)
        
        for button in [PLAY_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    six_men_morris()
                if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main()