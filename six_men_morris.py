import pygame 
import sys
import numpy as np
from button import Button
import random
import time
import math

pygame.init()

# COLORS
BG = pygame.Color("#32405C")
GREEN = pygame.Color("#009F92")
H_GREEN = pygame.Color("#00BFA5")
D_GREEN = pygame.Color("#00777B")
BLACK = pygame.Color("#101B3B")
RED = pygame.Color("#FE9E84")
H_RED = pygame.Color("#FDC4B4")
BLUE = pygame.Color("#6FA7FA")
H_BLUE = pygame.Color("#A1C5F9")
WHITE = pygame.Color("#F7E7BE")
H_WHITE = pygame.Color("#F8EDD4")

# GAME VARIABLES
ROW_COUNT = 5
COLUMN_COUNT = 5
SQUARESIZE = 110
board_width = COLUMN_COUNT * SQUARESIZE
board_height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 40)
X = np.nan # Place holder for null space, 0 = open space, 1 = player 1, 2 = player 2
PLAYER_PIECE = 1
H_PLAYER_PIECE = 11 # Highlighted player piece
AI_PIECE = 2
H_AI_PIECE = 12 # Highlighted AI piece
PLAYER_TURN = 0
AI_TURN = 1
highlighted_piece = None
all_piece_placed = False

# SCREEN VARIABLES
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MINIMAX AI")


# MINIMAX ALGORITHM
def minimax(board, depth, alpha, beta, maximizingPlayer, phase):
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if all_piece_placed:
            if is_terminal:
                if game_over(board, PLAYER_PIECE):
                    return 100000000000000
                elif game_over(board, AI_PIECE):
                    return -100000000000000
                else:
                    return 0
            else:
                print("Evaluating board")
                return evaluate_board(board, AI_PIECE, PLAYER_PIECE, phase)
        else:
            return evaluate_board(board, AI_PIECE, PLAYER_PIECE, phase)

    if maximizingPlayer:
        maxEval = -math.inf
        if phase == 1:
            for move in get_possible_moves(board, AI_PIECE):
                new_board = make_move(board, move, AI_PIECE)
                eval = minimax(new_board, depth - 1, alpha, beta, False, phase)
                maxEval = max(maxEval, eval)                
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff 
            return maxEval           
        elif phase == 2:
            for move in get_new_piece_moves(board, AI_PIECE):
                new_board = make_move(board, move, AI_PIECE)
                eval = minimax(new_board, depth - 1, alpha, beta, False, phase)
                maxEval = max(maxEval, eval)                
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff 
            return maxEval      
        else:
            for move in global_piece_moves(board, AI_PIECE):
                new_board = fly_move(board, move, AI_PIECE)
                eval = minimax(new_board, depth - 1, alpha, beta, False, phase)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return maxEval
    else:
        minEval = math.inf
        if phase == 1:
            for move in get_possible_moves(board, PLAYER_PIECE):
                new_board = make_move(board, move, PLAYER_PIECE)
                eval = minimax(new_board, depth - 1, alpha, beta, True, phase)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return minEval
        elif phase == 2:
            for move in get_new_piece_moves(board, PLAYER_PIECE):
                new_board = make_move(board, move, PLAYER_PIECE)
                eval = minimax(new_board, depth - 1, alpha, beta, True, phase)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return minEval
        else:
            for move in global_piece_moves(board, PLAYER_PIECE):
                new_board = fly_move(board, move, PLAYER_PIECE)
                eval = minimax(new_board, depth - 1, alpha, beta, True, phase)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
        

def is_terminal_node(board):
    return  game_over(board, AI_PIECE) or game_over(board, PLAYER_PIECE)
 
def find_best_move(board, phase):
    best_score = -math.inf
    best_move = None
    depth = 2
    if phase == 1:
        for move in get_possible_moves(board, AI_PIECE):
            new_board = make_move(board, move, AI_PIECE)
            score = minimax(new_board, depth, -math.inf, math.inf, False, phase)
            if score > best_score:
                best_score = score
                best_move = move 
    elif phase == 2:
        for move in get_new_piece_moves(board, AI_PIECE):
            new_board = make_move(board, move, AI_PIECE)
            score = minimax(new_board, depth, -math.inf, math.inf, False, phase)
            if score > best_score:
                best_score = score
                best_move = move
    else:
        for move in global_piece_moves(board, AI_PIECE):
            new_board = fly_move(board, move, AI_PIECE)
            score = minimax(new_board, depth, -math.inf, math.inf, False, phase)
            if score > best_score:
                best_score = score
                best_move = move

    return best_move

def game_over(board, piece):
    # Check if a player has only two pieces left
    if np.sum(board == piece) <= 2:
        return True
    if len(get_possible_moves(board, piece)) == 0:
        return True
    if len(get_new_piece_moves(board, piece)) == 0:
        return True
    if len(global_piece_moves(board, piece)) == 0:
        return True
    return False

def get_possible_moves(board, piece):
    possible_moves = []
    # Check for empty spots to place a new piece
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                possible_moves.append(((r, c), None))  # None indicates a new piece placement
    return possible_moves

def get_new_piece_moves(board, piece):
    # Check for existing pieces that can be moved
    possible_moves = []
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                # Check all adjacent spots
                corners = [(0, 0), (0, 4), (4, 0), (4, 4)] 
                vertical_middle_corners = [(0, 2), (4, 2)]
                horizontal_middle_corners = [(2, 0), (2, 4)]
                if (r, c) in corners: # We'll be checking two steps away from the corner since, it's blocked by null space
                    adjacent_positions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
                elif (r, c) in vertical_middle_corners: # We'll be checking two steps away from the vertical middle corners
                    adjacent_positions = [(-1, 0), (1, 0), (0, -2), (0, 2)]
                elif (r, c) in horizontal_middle_corners: # We'll be checking two steps away from the horizontal middle corners
                    adjacent_positions = [(-2, 0), (2, 0), (0, -1), (0, 1)]
                else:
                    adjacent_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dr, dc in adjacent_positions:
                    new_r, new_c = r + dr, c + dc
                    if 0 <= new_r < ROW_COUNT and 0 <= new_c < COLUMN_COUNT and board[new_r][new_c] == 0:
                        possible_moves.append(((r, c), (new_r, new_c)))
    return possible_moves

def global_piece_moves(board, piece):
    # Check for existing pieces that can be moved
    possible_moves = []
    # Check for empty spots to place a new piece
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                for dr in range(ROW_COUNT):
                    for dc in range(COLUMN_COUNT):
                        if board[dr][dc] == 0:
                            possible_moves.append(((r, c), (dr, dc)))         
    return possible_moves

def make_move(board, move, piece):
    new_board = np.copy(board)
    if move[1] == None:  # New piece
        row, col = move[0]
        new_board[row][col] = piece
    else:  # Placing a new piece
        print("Move: ", move)
        (r1, c1), (r2, c2) = move
        new_board[r1][c1] = 0
        new_board[r2][c2] = piece 
    return new_board

def fly_move(board, move, piece):
    new_board = np.copy(board)
    (r1, c1), (r2, c2) = move
    new_board[r1][c1] = 0
    new_board[r2][c2] = piece 
    return new_board

def evaluate_board(board, player_piece, opponent_piece, phase):
    player_score = 0
    opponent_score = 0
    
    # Count pieces on the board
    player_pieces = np.sum(board == player_piece)
    opponent_pieces = np.sum(board == opponent_piece)
    
    # Calculate actual mills
    player_actual_mills = count_actual_mills(board, player_piece)
    opponent_actual_mills = count_actual_mills(board, opponent_piece)
    
    # Calculate potential mills
    player_potential_mills = count_potential_mills(board, player_piece)
    opponent_potential_mills = count_potential_mills(board, opponent_piece)
    
    # Calculate threats
    player_threats = count_threats(board, player_piece)
    opponent_threats = count_threats(board, opponent_piece)
    
    # Evaluate board state
    player_score += player_pieces * 10  
    player_score += player_actual_mills * 50  
    player_score += player_potential_mills * 100  
    player_score += player_threats * 100  
    player_score += positional_advantage(board, player_piece)  
    player_score += adaptability(board, player_piece, phase)  
    
    opponent_score += opponent_pieces * 10
    opponent_score += opponent_actual_mills * 50
    opponent_score += opponent_potential_mills * 100
    opponent_score += opponent_threats * 30
    opponent_score += positional_advantage(board, opponent_piece)
    opponent_score += adaptability(board, opponent_piece, phase)

    total_score = player_score - opponent_score
    print("Total score: ", total_score)
    
    return total_score # Return the score difference

def count_actual_mills(board, piece):
    actual_mills = 0
    # Check rows
    for row in range(ROW_COUNT):
        if row != 2 and [board[row][c] for c in range(ROW_COUNT)].count(piece) == 3:
            actual_mills += 50
            
    # Check columns
    for col in range(COLUMN_COUNT):
       if col != 2 and [board[r][col] for r in range(COLUMN_COUNT)].count(piece) == 3:
            actual_mills += 50
    return actual_mills

def count_potential_mills(board, piece):
    potential_mills = 0
    # Iterate over all positions on the board
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            # Check if the position is empty
            if board[r][c] == 0:
                # Temporarily place the piece at the position
                board[r][c] = piece
                # Check if this forms a mill
                if forms_mill(board, r, c, piece):
                    potential_mills += 100
                # Remove the piece from the position
                board[r][c] = 0
    return potential_mills

def forms_mill(board, row, col, piece):
    # Check all rows except the middle one for a mill
    for r in range(ROW_COUNT):
        if r != 2 and [board[row][c] for c in range(COLUMN_COUNT)].count(piece) == 3:
            return True

    # Check all columns except the middle one for a mill
    for c in range(COLUMN_COUNT):
        if c != 2 and [board[r][col] for r in range(ROW_COUNT)].count(piece) == 3:
            return True
    return False

def count_threats(board, piece):
    threats = 0
    # Iterate over all positions on the board
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            # Check if the position is empty
            if board[r][c] == 0:
                # Check if placing a piece at this position forms a threat
                if forms_threat(board, r, c, piece):
                    threats += 100
    return threats

def forms_threat(board, row, col, piece):
    # Check all rows except the middle one for a mill
    if row != 2 and [board[row][c] for c in range(COLUMN_COUNT)].count(piece) == 2:
        return True

    # Check all columns except the middle one for a mill
    if col != 2 and [board[r][col] for r in range(ROW_COUNT)].count(piece) == 2:
        return True
    
    return False

def calculate_positional_weights(board):
    weights = np.array([
        [50, X, 30, X, 50],
        [X, 18, 8, 18, X],
        [30, 8, X, 8, 30],
        [X, 18, 8, 18, X],
        [50, X, 30, X, 50]
    ])
    
    # Assign weights based on adjacency to opponent's pieces
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r, c] == 0:  # Check only empty positions
                if r > 0 and board[r - 1, c] == PLAYER_PIECE:
                    weights[r, c] += 1
                if r < 4 and board[r + 1, c] == PLAYER_PIECE:
                    weights[r, c] += 1
                if c > 0 and board[r, c - 1] == PLAYER_PIECE:
                    weights[r, c] += 1
                if c < 4 and board[r, c + 1] == PLAYER_PIECE:
                    weights[r, c] += 1
    return weights

def positional_advantage(board, piece):
    # Define weights for different board positions
    position_weights = calculate_positional_weights(board)
    advantage = 0
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                advantage += position_weights[r][c]
    return advantage

def adaptability(board, piece, phase):
    # Evaluate adaptability based on the number of available moves
    adaptability_score = 0
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 0:
                if phase == 1:
                    adaptability_score += len(get_possible_moves(board, piece))
                elif phase == 2:
                    adaptability_score += len(get_new_piece_moves(board, piece))
                else:
                    adaptability_score += len(global_piece_moves(board, piece))
    return adaptability_score

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

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, row, col):
    return board[row][col] == 0

def is_occupied(board, row, col):
    return board[row][col] != 0

def is_adjacent_empty(board, row, col):
    corners = [(0, 0), (0, 4), (4, 0), (4, 4)] 
    vertical_middle_corners = [(0, 2), (4, 2)]
    horizontal_middle_corners = [(2, 0), (2, 4)]
    if (row, col) in corners: # We'll be checking two steps away from the corner since, it's blocked by null space
        adjacent_positions = [(row - 2, col), (row + 2, col), (row, col - 2), (row, col + 2)]
    elif (row, col) in vertical_middle_corners: # We'll be checking two steps away from the vertical middle corners
        adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 2), (row, col + 2)]
    elif (row, col) in horizontal_middle_corners: # We'll be checking two steps away from the horizontal middle corners
        adjacent_positions = [(row - 2, col), (row + 2, col), (row, col - 1), (row, col + 1)]
    else:
        adjacent_positions = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    for r, c in adjacent_positions:
        if 0 <= r < ROW_COUNT and 0 <= c < COLUMN_COUNT and board[r][c] == 0:
            return True
    return False

def is_mill(board, row, col, piece):
    # Prevent horizontal middle row from forming a mill
    if [board[2][c] for c in range(COLUMN_COUNT)].count(piece) == 3:
        return False
    # Prevent vertical middle column from forming a mill
    if [board[r][2] for r in range(ROW_COUNT)].count(piece) == 3:
        return False
    # Check row
    if [board[r][col] for r in range(ROW_COUNT)].count(piece) == 3:
        return True
    # Check column
    if [board[row][c] for c in range(COLUMN_COUNT)].count(piece) == 3:
        return True
    return False

def remove_piece(board, piece):
    width_center = (screen_width/2) - (board_width/2) # Starting point of board width
    removing = True
    print_board(board)
    draw_board(board)

    while removing:
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
                    if board[row][col] == piece:
                        if is_mill(board, row, col, piece):
                            font = get_font(29, 1)
                            text = font.render("YOU CANNOT REMOVE A PIECE FROM A MILL", True, RED)
                            screen.blit(text, (width_center - 20, screen_height - 60))
                        else:
                            print("Piece found")
                            board[row][col] = 0
                            print("Piece removed")
                            removing = False
                    else:  
                        print("Incorrect piece")
                        print("(", row, col, ")")
                        print_board(board)
                        draw_board(board)
        pygame.display.update()
    
def ai_remove_piece(board, piece):
    removing = True
    player_pieces = []
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                player_pieces.append((r, c))
    
    player_piece_to_remove = random.choice(player_pieces)
    while removing:
        row, col = player_piece_to_remove
        if is_mill(board, row, col, piece):
            player_pieces.remove(player_piece_to_remove)
            player_piece_to_remove = random.choice(player_pieces)
            row, col = player_piece_to_remove
        else:
            board[row][col] = 0
            removing = False
    player_pieces.clear()
                
    
def winning_move(piece_count):
    if piece_count <= 2:
        return True
    return False

def game_over_screen(board, winner):
    game_bg = pygame.image.load("assets/GAME BG.png")
    screen.blit(game_bg, (0, 0))
    font = get_font(29, 1)
    if winner == 1:
        font = get_font(35, 1)
        text = font.render("PLAYER WINS", True, BLUE)
        screen.blit(text, (screen_width//2 - text.get_width()//2, 60))
    else: 
        font = get_font(35, 1)
        text = font.render("AI WINS", True, RED)
        screen.blit(text, (screen_width//2 - text.get_width()//2, 60))

    print_board(board)
    draw_board(board)
    waiting = True

    while waiting:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=None, pos=(screen_width//2 - 75, screen_height - 30), 
                            text_input="MENU", font=get_font(30, 1), base_color=WHITE, hovering_color=RED)
        QUIT_BUTTON = Button(image=None, pos=(screen_width//2 + 75, screen_height - 30), 
                            text_input="QUIT", font=get_font(30, 1), base_color=WHITE, hovering_color=RED)
        
        for button in [MENU_BUTTON, QUIT_BUTTON]:
            button.changeColor(GAME_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(GAME_MOUSE_POS):
                    main()
                if QUIT_BUTTON.checkForInput(GAME_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    
                    
def highlt_existing(board, piece):
    if any(piece in sublist for sublist in board):
        return True
    
def draw_remaining_pieces(player_pieces, ai_pieces):
    font = get_font(29, 1)
    piece_count = 6
    text = font.render("PLAYER PIECES LEFT: ", True, WHITE)
    screen.blit(text, (20, 60))
    print("Player pieces left: ", player_pieces)
    remaining_player_pieces = piece_count - player_pieces
    for i in range(remaining_player_pieces):
        pygame.draw.circle(screen, BLUE, (20 + 20 + i * 40, 120), RADIUS)
    
    text = font.render("AI PIECES LEFT: ", True, WHITE)
    screen.blit(text, (20, 160))
    print("AI pieces left: ", ai_pieces)
    remaining_ai_pieces = piece_count - ai_pieces
    for i in range(remaining_ai_pieces):
        pygame.draw.circle(screen, RED, (20 + 20 + i * 40, 220), RADIUS)
    pygame.display.update()

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
            if not np.isnan(board[r][c]): # Which is the null space
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
            elif board[r][c] == 11:
                pygame.draw.circle(screen, H_BLUE, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, SQUARESIZE+int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS+15)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, RED, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, SQUARESIZE+int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS+15)
            elif board[r][c] == 12:
                pygame.draw.circle(screen, H_RED, ((int(c*SQUARESIZE+SQUARESIZE/2))+width_center, SQUARESIZE+int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS+15)   
    pygame.display.update()

def six_men_morris():
    game_bg = pygame.image.load("assets/GAME BG.png")
    screen.blit(game_bg, (0, 0))
    playing = True
    width_center = (screen_width/2) - (board_width/2) # Starting point of board width
    turn = random.randint(PLAYER_TURN, AI_TURN)
    PLAYER_MAX_PIECES = 6
    AI_MAX_PIECES = 6
    PLAYER_COUNT = 0
    AI_COUNT = 0
    highlighted_piece = None
    phase_2 = False

    board = create_board()
    print_board(board)
    draw_board(board)
    draw_remaining_pieces(PLAYER_COUNT, AI_COUNT)

    while playing:
        GAME_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=None, pos=(75,30), 
                            text_input="MENU", font=get_font(29, 1), base_color=WHITE, hovering_color=RED)
        RESET_BUTTON = Button(image=None, pos=(75, screen_height-30), 
                            text_input="RESET", font=get_font(29, 1), base_color=WHITE, hovering_color=RED)
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
                posx = event.pos[0] # X coordinate
                posy = event.pos[1] # Y coordinate
                # Will only accept x and y coordinates within the board parameters
                if width_center <= posx <= (width_center + board_width) and SQUARESIZE <= posy <= (board_height):
                    col = int((posx - width_center) // SQUARESIZE)
                    row = int((posy - SQUARESIZE) // SQUARESIZE)

                    if turn == PLAYER_TURN:                                    
                        if PLAYER_COUNT < PLAYER_MAX_PIECES:
                            print("(", row, col, ")")
                            if is_valid_location(board, row, col):
                                drop_piece(board, row, col, PLAYER_PIECE)
                                PLAYER_COUNT += 1
                                pygame.draw.rect(screen, BG, (20, 60, 300, 200))  
                                if is_mill(board, row, col, PLAYER_PIECE):
                                    font = get_font(29, 1)
                                    text = font.render("MILL FORMED: REMOVE ONE OF AI PIECES", True, BLUE)
                                    screen.blit(text, (width_center - 10, 60))
                                    remove_piece(board, AI_PIECE) # Update maximum AI pieces
                                    screen.blit(game_bg, (0, 0))
                                    AI_MAX_PIECES -= 1
                                    AI_COUNT -= 1                
                                turn += 1
                                turn = turn % 2
                                draw_remaining_pieces(PLAYER_COUNT, AI_COUNT)

                        else:
                            phase_2 = True
                            all_piece_placed = True
                        
                        if phase_2:
                            if is_occupied(board, row, col):
                                if board[row][col] == PLAYER_PIECE:
                                    print("Clicked on player piece")
                                    if not highlt_existing(board, H_PLAYER_PIECE):
                                        drop_piece(board, row, col, H_PLAYER_PIECE)
                                        highlighted_piece = (row, col)  # Store the location of the highlighted piece
                                elif board[row][col] == H_PLAYER_PIECE:
                                    print("Clicked on highlighted player piece")
                                    drop_piece(board, row, col, PLAYER_PIECE)
                                    highlighted_piece = None  # Clear the highlighted piece location
                            elif highlighted_piece is not None:  # If a piece is highlighted
                                if PLAYER_COUNT & PLAYER_MAX_PIECES > 3:
                                    if is_adjacent_empty(board, highlighted_piece[0], highlighted_piece[1]):
                                        # Move the highlighted piece to the new location
                                        board[highlighted_piece[0]][highlighted_piece[1]] = 0
                                        drop_piece(board, row, col, PLAYER_PIECE) 
                                        if is_mill(board, row, col, PLAYER_PIECE):
                                            if is_mill(board, row, col, AI_PIECE):
                                                font = get_font(29, 1)
                                                text = font.render("NO AI PIECES CAN BE REMOVED", True, BLUE)
                                                screen.blit(text, (screen_width//2 - text.get_width(), 60))
                                            else:
                                                font = get_font(29, 1)
                                                text = font.render("MILL FORMED: REMOVE ONE OF AI PIECES", True, BLUE)
                                                screen.blit(text, (width_center - 10, 60))
                                                remove_piece(board, AI_PIECE) # Update maximum AI pieces
                                                screen.blit(game_bg, (0, 0))
                                                AI_MAX_PIECES -= 1
                                                AI_COUNT -= 1
                                                print("AI pieces left: ", AI_MAX_PIECES) 
                                                if all_piece_placed:
                                                    print("All pieces placed")
                                                    if winning_move(AI_COUNT):
                                                        game_over_screen(board, 1) 
                                        highlighted_piece = None  # Clear the highlighted piece location
                                        turn += 1
                                        turn = turn % 2
                                        
                                else:
                                    board[highlighted_piece[0]][highlighted_piece[1]] = 0
                                    drop_piece(board, row, col, PLAYER_PIECE) 
                                    if is_mill(board, row, col, PLAYER_PIECE):
                                        if is_mill(board, row, col, AI_PIECE):
                                            font = get_font(29, 1)
                                            text = font.render("NO AI PIECES CAN BE REMOVED", True, BLUE)
                                            screen.blit(text, (screen_width//2 - text.get_width(), 60))
                                        else:
                                            font = get_font(29, 1)
                                            text = font.render("MILL FORMED: REMOVE ONE OF AI PIECES", True, BLUE)
                                            screen.blit(text, (width_center - 10, 60))
                                            remove_piece(board, AI_PIECE) # Update maximum AI pieces
                                            screen.blit(game_bg, (0, 0))
                                            AI_MAX_PIECES -= 1
                                            AI_COUNT -= 1
                                            print("AI pieces left: ", AI_MAX_PIECES) 
                                            if all_piece_placed:
                                                print("All pieces placed")
                                                if winning_move(AI_COUNT):
                                                    game_over_screen(board, 1)
                                    highlighted_piece = None  # Clear the highlighted piece location
                                    turn += 1
                                    turn = turn % 2                           
                                    
                            print_board(board)
                            draw_board(board)
                            
                if MENU_BUTTON.checkForInput(GAME_MOUSE_POS):
                    main()
                if RESET_BUTTON.checkForInput(GAME_MOUSE_POS):
                    board = create_board()
                    turn = random.randint(PLAYER_TURN, AI_TURN)
                    PLAYER_COUNT, AI_COUNT = 0, 0
                    PLAYER_MAX_PIECES, AI_MAX_PIECES = 6, 6
                if QUIT_BUTTON.checkForInput(GAME_MOUSE_POS):
                    pygame.quit()
                    sys.exit()                     
                            
            if turn == AI_TURN:   
                if AI_COUNT < AI_MAX_PIECES:
                    print("Phase 1")
                    move = find_best_move(board, 1)
                    ai_row, ai_col = move[0]
                    if is_valid_location(board, ai_row, ai_col):
                        print("(", ai_row, ai_col, ")")  
                        drop_piece(board, ai_row, ai_col, AI_PIECE)
                        pygame.draw.rect(screen, BG, (20, 60, 300, 200))  
                        pygame.draw.rect(screen, BG, (width_center, screen_height - 50, board_width, SQUARESIZE))
                        font = get_font(29, 1)
                        text = font.render(f"AI MOVE: ({ai_row}, {ai_col})", True, RED)
                        screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height - 50)) 
                        AI_COUNT += 1  
                        if is_mill(board, ai_row, ai_col, AI_PIECE):
                            ai_remove_piece(board, PLAYER_PIECE) # Update maximum AI pieces
                            PLAYER_MAX_PIECES -= 1
                            PLAYER_COUNT -= 1
                            print("PLAYER pieces left: ", PLAYER_MAX_PIECES) 
                        turn += 1
                        turn = turn % 2 
                        print_board(board)
                        draw_board(board)  
                        draw_remaining_pieces(PLAYER_COUNT, AI_COUNT)  
                        
                else:
                    pygame.draw.rect(screen, BG, (20, 60, 300, 200))  
                    phase_2 = True
                    all_piece_placed = True

                if phase_2:
                    if AI_COUNT & AI_MAX_PIECES > 3:
                        print("Phase 2")
                        old_loc, new_loc = find_best_move(board, 2)                        
                    else:
                        print("Phase 3")
                        old_loc, new_loc = find_best_move(board, 3)
                    
                    if old_loc and new_loc is not None:
                        ai_row, ai_col = old_loc
                        ai_new_row, ai_new_col = new_loc
                        print("(", ai_row, ai_col, ") to (", ai_new_row, ai_new_col, ")")
                        board[ai_row][ai_col] = 0
                        drop_piece(board, ai_new_row, ai_new_col, AI_PIECE)
                        pygame.draw.rect(screen, BG, (width_center, screen_height - 50, board_width, SQUARESIZE))
                        font = get_font(29, 1)
                        text = font.render(f"AI MOVE: ({ai_row}, {ai_col}) to ({ai_new_row}, {ai_new_col})", True, RED)
                        screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height - 50)) 
                        if is_mill(board, ai_new_row, ai_new_col, AI_PIECE):
                            ai_remove_piece(board, PLAYER_PIECE) # Update maximum AI pieces      
                            PLAYER_MAX_PIECES -= 1
                            PLAYER_COUNT -= 1
                            print("PLAYER pieces left: ", PLAYER_MAX_PIECES)     
                            if all_piece_placed:
                                if winning_move(PLAYER_COUNT): #Checks if the player has only two pieces left
                                    game_over_screen(board, 2)
                        turn += 1
                        turn = turn % 2                              
                    else:
                        game_over_screen(board, 2)
    
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
    background = pygame.image.load("assets/MENU BG.png")
    screen.blit(background, (0, 0))
    while running:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button(image=None, pos=(screen_width//2 + 15, 385), 
                            text_input="PLAY GAME", font=get_font(68, 1), base_color=WHITE, hovering_color=H_WHITE)
        CONTROLS_BUTTON = Button(image=None, pos=(screen_width//2 + 15, 485), 
                            text_input="CONTROLS", font=get_font(68, 1), base_color=WHITE, hovering_color=H_WHITE)
        QUIT_BUTTON = Button(image=None, pos=(screen_width//2 + 15, 585), 
                            text_input="QUIT GAME", font=get_font(68, 1), base_color=RED, hovering_color=H_RED)
        
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