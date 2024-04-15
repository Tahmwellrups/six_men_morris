import pygame 
import sys
import numpy as np
from button import Button
import random

pygame.init()

# COLORS
BG = pygame.Color("#32405C")
GREEN = pygame.Color("#009F92")
D_GREEN = pygame.Color("#00777B")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FE9E84")
H_RED = pygame.Color("#FFAAAC")
BLUE = pygame.Color("#6FA7FA")
H_YELLOW = pygame.Color("#EBE6B6")
WHITE = pygame.Color("#F7E7BE")

# GAME VARIABLES
ROW_COUNT = 5
COLUMN_COUNT = 5
SQUARESIZE = 110
board_width = COLUMN_COUNT * SQUARESIZE
board_height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 40)
X = 3 # Place holder for null space, 0 = open space, 1 = player 1, 2 = player 2
PLAYER_PIECE = 1
AI_PIECE = 2
PLAYER_TURN = 0
AI_TURN = 1

# SCREEN VARIABLES
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MINIMAX AI")

# GAME FUNCTIONS
def create_board(): # X = null space
    board = np.array([
        [0, X, 0, X, 0],
        [X, 0, 0, 0, X],
        [0, 0, X, 0, 0],
        [X, 0, 0, 0, X],
        [0, X, 0, X, 0]
    ])
    return board

def print_board(board):
    print(board)

def is_valid_location(board, row, col):
    return board[row][col] == 0

def drop_piece(board, row, col, player):
    if player == 1:
        board[row][col] = 1
    else: 
        board[row][col] = 2

def draw_lines():
    width_center = (screen_width / 2) - (board_width / 2)
    # Coordinates of the outside positions
    outside_positions = [
        ((0, 0), (0, 4)),
        ((0, 0), (4, 0)),
        ((4, 0), (4, 4)),
        ((0, 4), (4, 4))
    ]
    # Draw lines between the outside positions
    for pos1, pos2 in outside_positions:
        pygame.draw.line(screen, WHITE, 
                        (pos1[1] * SQUARESIZE + SQUARESIZE / 2 + width_center, pos1[0] * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE),
                        (pos2[1] * SQUARESIZE + SQUARESIZE / 2 + width_center, pos2[0] * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE), 5)
    # Coordinates of the inside positions
    inside_positions = [
        ((1, 1), (1, 3)),
        ((1, 1), (3, 1)),
        ((3, 1), (3, 3)),
        ((1, 3), (3, 3)),
        ((0, 2), (1, 2)),
        ((2, 0), (2, 1)),
        ((2, 3), (2, 4)),
        ((3, 2), (4, 2))   
    ]
    # Draw lines between the inside positions
    for pos1, pos2 in inside_positions:
        pygame.draw.line(screen, WHITE, 
                        (pos1[1] * SQUARESIZE + SQUARESIZE / 2 + width_center, pos1[0] * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE),
                        (pos2[1] * SQUARESIZE + SQUARESIZE / 2 + width_center, pos2[0] * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE), 5)

def draw_board(board):
    width_center = (screen_width/2) - (board_width/2)
    # Board
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] != X: # Which is the null space
                pygame.draw.rect(screen, GREEN, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            else:
                pygame.draw.rect(screen, D_GREEN, ((c*SQUARESIZE)+width_center, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
    # Lines
    draw_lines()
    # Pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == 0:
                pygame.draw.circle(screen, WHITE, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, SQUARESIZE+int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 1: 
                pygame.draw.circle(screen, BLUE, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, SQUARESIZE+int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS+15)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, RED, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, SQUARESIZE+int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS+15)
    pygame.display.update()

def six_men_morris():
    screen.fill(BG)
    playing = True
    width_center = (screen_width/2) - (board_width/2) # Starting point of board width
    turn = random.randint(PLAYER_TURN, AI_TURN)
    MAX_PIECES = 6
    PLAYER_COUNT = 0
    AI_COUNT = 0

    board = create_board()
    print_board(board)
    draw_board(board)

    while playing:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=None, pos=(75,30), 
                            text_input="MENU", font=get_font(29, 1), base_color=WHITE, hovering_color=RED)
        RESET_BUTTON = Button(image=None, pos=(75, screen_height-30), 
                            text_input="RESET", font=get_font(29, 1), base_color=WHITE, hovering_color=RED)
        QUIT_BUTTON = Button(image=None, pos=(screen_width-75, screen_height-30), 
                            text_input="QUIT", font=get_font(29, 1), base_color=WHITE, hovering_color=RED)
        
        for button in [MENU_BUTTON, RESET_BUTTON, QUIT_BUTTON]:
            button.changeColor(GAME_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0] # X coordinate
                posy = event.pos[1] # Y coordinate
                # Will only accept x and y coordinates within the board parameters
                if width_center <= posx <= (width_center + board_width) and SQUARESIZE <= posy <= (board_height):
                    col = int((posx - width_center) // SQUARESIZE)
                    row = int((posy - SQUARESIZE) // SQUARESIZE)
                    # If the square is clicked it will highlight, else it will erase the highlight
                    if is_valid_location(board, row, col):
                        print("(", row, col, ")")
                        if turn == PLAYER_TURN and PLAYER_COUNT < MAX_PIECES: 
                            drop_piece(board, row, col, PLAYER_PIECE)
                            PLAYER_COUNT += 1
                            turn += 1
                            turn = turn % 2
                        elif turn == AI_TURN and AI_COUNT < MAX_PIECES:
                            drop_piece(board, row, col, AI_PIECE)
                            AI_COUNT += 1
                            turn += 1
                            turn = turn % 2
                if MENU_BUTTON.checkForInput(GAME_MOUSE_POS):
                    main()
                if RESET_BUTTON.checkForInput(GAME_MOUSE_POS):
                    board = create_board()
                    turn = random.randint(PLAYER_TURN, AI_TURN)
                if QUIT_BUTTON.checkForInput(GAME_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

                print_board(board)
                draw_board(board)

        pygame.display.update()

#  MENU FUNCTIONS
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