# Vikram Bawa
# 2020-12-23
# 2 player chess
import pygame
import time
import math
import copy
import random

# Initializes all pygame modules.
pygame.init()

# The current game state from white's perspective.
state = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
         ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["--", "--", "--", "--", "--", "--", "--", "--"],
         ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
         ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

# The current game state from black's perspective.
reverse = [["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
           ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
           ["--", "--", "--", "--", "--", "--", "--", "--"],
           ["--", "--", "--", "--", "--", "--", "--", "--"],
           ["--", "--", "--", "--", "--", "--", "--", "--"],
           ["--", "--", "--", "--", "--", "--", "--", "--"],
           ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
           ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]

# Ratings of pawn positions.
PAWN = [[0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [-5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]]

# Ratings of knight positions.
KNIGHT = [[-50, -40, -30, -30, -30, -30, -40, -50],
          [-40, -20, 0, 0, 0, 0, -20, -40],
          [-30, 0, 10, 15, 15, 10, 0, -30],
          [-30, 5, 15, 20, 20, 15, 5, -30],
          [-30, 0, 15, 20, 20, 15, 0, -30],
          [-30, 5, 10, 15, 15, 10, 5, -30],
          [-40, -20, 0, 5, 5, 0, -20, -40],
          [-50, -40, -30, -30, -30, -30, -40, -50]]

# Ratings of bishop positions.
BISHOP = [[-20, -10, -10, -10, -10, -10, -10, -20],
          [-10, 0, 0, 0, 0, 0, 0, -10],
          [-10, 0, 5, 10, 10, 5, 0, -10],
          [-10, 5, 5, 10, 10, 5, 5, -10],
          [-10, 0, 10, 10, 10, 10, 0, -10],
          [-10, 10, 10, 10, 10, 10, 10, -10],
          [-10, 5, 0, 0, 0, 0, 5, -10],
          [-20, -10, -10, -10, -10, -10, -10, -20]]

# Ratings of rook positions.
ROOK = [[0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]]

# Ratings of queen positions.
QUEEN = [[-20, -10, -10, -5, -5, -10, -10, -20],
         [-10, 0, 0, 0, 0, 0, 0, -10],
         [-10, 0, 5, 5, 5, 5, 0, -10],
         [-5, 0, 5, 5, 5, 5, 0, -5],
         [0, 0, 5, 5, 5, 5, 0, -5],
         [-10, 5, 5, 5, 5, 5, 0, -10],
         [-10, 0, 5, 0, 0, 0, 0, -10],
         [-20, -10, -10, -5, -5, -10, -10, -20]]

# Ratings of king positions in the middle game.
KING_MID = [[-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -40, -40, -30, -30, -20],
                [-10, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20]]

# Ratings of king positions in the end game.
KING_END = [[-50, -40, -30, -20, -20, -30, -40, -50],
            [-30, -20, -10, 0, 0, -10, -20, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -30, 0, 0, 0, 0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50]]

# Will contain all board states.
all_states = []

# Will contain locations of all images that will be used.
img = {}

# Variables for visuals.
scale_factor = 0.5
tile_size = round(200 * scale_factor)
width = 8 * tile_size
height = 8 * tile_size
board_size = 8
fps = 60

# Different fun values change board colour.
fun_time = 1

# castle[0] is if white can king side castle, castle[1] is white's queen side castle,
# castle[2] is black's king side castle, and castle[3] is black's queen side castle.
castle = [True, True, True, True]

# Keeps track of how many moves its been since a pawn move or piece capture.
fifty_move_rule_counter = 0

# mode = 1 is player vs player, mode = 0 is player vs computer (mode = 0 in progress still).
mode = 1

# If looking from white's perspective, this is "w", otherwise it is "b".
perspective = "w"


# Description:    Gives a decent move to play in the given board state.
# Pre-condition:  current_state is a legal board state of chess
#                 previous_state is the legal board state immediately before current_state
#                 depth is a non-negative integer
#                 alpha is always initialized to negative infinity
#                 beta is always initialized to positive infinity
#                 colour is either "w" for white or "b" for black
#                 castling is an array of four booleans
# Post-condition: Returns a move to play and its evaluation; negative evaluation favours black, positive favours white.
def mini_max(current_state, previous_state, depth, alpha, beta, colour, castling):
    if depth == 0 or not available_moves(colour, current_state, previous_state, castling):
        if colour == "w":
            other = "b"
        else:
            other = "w"
        return [evaluate(current_state, other), []]

    best_move = []

    if colour == "w":
        max_evaluation = -math.inf
        for move in available_moves(colour, current_state, previous_state, castling):
            previous_state = copy.deepcopy(current_state)
            make = make_move(current_state, move, castling)
            current_state = copy.deepcopy(make[0])
            castling = copy.deepcopy(make[1])
            evaluation = mini_max(current_state, previous_state, depth - 1, alpha, beta, "b", castling)[0]
            if max_evaluation < evaluation:
                max_evaluation = evaluation
                best_move = copy.deepcopy(move)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return [max_evaluation, best_move]
    else:
        min_evaluation = math.inf
        for move in available_moves(colour, current_state, previous_state, castling):
            previous_state = copy.deepcopy(current_state)
            make = make_move(current_state, move, castling)
            current_state = copy.deepcopy(make[0])
            castling = copy.deepcopy(make[1])
            evaluation = mini_max(current_state, previous_state, depth - 1, alpha, beta, "w", castling)[0]
            if min_evaluation > evaluation:
                min_evaluation = evaluation
                best_move = copy.deepcopy(move)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return [min_evaluation, best_move]


# Description:    Performs a move on a state.
# Pre-condition:  current_state is a legal board state of chess, move is a legal move for current_state, and
#                 castling is an array of four booleans.
# Post-condition: Return the new current_state and castling array.
def make_move(current_state, move, castling):
    if current_state[move[0][0]][move[0][1]] == "wK" and move[0][1] == move[1][1] - 2 and castling[0]:
        current_state[7][4] = "--"
        current_state[7][7] = "--"
        current_state[7][6] = "wK"
        current_state[7][5] = "wR"
        castling[0] = False
        castling[1] = False
    elif current_state[move[0][0]][move[0][1]] == "wK" and move[0][1] == move[1][1] + 2 and castling[1]:
        current_state[7][4] = "--"
        current_state[7][0] = "--"
        current_state[7][2] = "wK"
        current_state[7][3] = "wR"
        castling[0] = False
        castling[1] = False
    elif current_state[move[0][0]][move[0][1]] == "bK" and move[0][1] == move[1][1] - 2 and castling[2]:
        current_state[0][4] = "--"
        current_state[0][7] = "--"
        current_state[0][6] = "bK"
        current_state[0][5] = "bR"
        castling[2] = False
        castling[3] = False
    elif current_state[move[0][0]][move[0][1]] == "bK" and move[0][1] == move[1][1] + 2 and castling[3]:
        current_state[0][4] = "--"
        current_state[0][0] = "--"
        current_state[0][2] = "bK"
        current_state[0][3] = "bR"
        castling[2] = False
        castling[3] = False
    elif current_state[move[0][0]][move[0][1]] == "wP" and move[1][0] == 0:
        current_state[move[0][0]][move[0][1]] = "--"
        current_state[move[1][0]][move[1][1]] = "wQ"
    elif current_state[move[0][0]][move[0][1]] == "bP" and move[1][0] == 7:
        current_state[move[0][0]][move[0][1]] = "--"
        current_state[move[1][0]][move[1][1]] = "bQ"
    else:
        current_state[move[1][0]][move[1][1]] = current_state[move[0][0]][move[0][1]]
        current_state[move[0][0]][move[0][1]] = "--"
        if move[0] == (7, 7):
            castling[0] = False
        elif move[0] == (7, 0):
            castling[1] = False
        elif move[0] == (0, 7):
            castling[2] = False
        elif move[0] == (0, 0):
            castling[3] = False
        elif move[0] == (7, 4):
            castling[0] = False
            castling[1] = False
        elif move[0] == (0, 4):
            castling[2] = False
            castling[3] = False
    return [current_state, castling]


# Description:    Returns an evaluation of the input board state. Positive favours white, negative favours black.
# Pre-condition:  current_state is a legal board state of chess and other is either "w" for white or "b" for black.
# Post-condition: An integer is returned; it is positive if white is favoured, and negative if black is favoured.
def evaluate(current_state, other):
    total = 0
    if not king_safe(current_state, other):
        if other == "b":
            return math.inf
        else:
            return -math.inf
    for row in range(board_size):
        for col in range(board_size):
            if "w" in current_state[row][col]:
                if "P" in current_state[row][col]:
                    total += 100 + PAWN[row][col]
                elif "N" in current_state[row][col]:
                    total += 320 + KNIGHT[row][col]
                elif "B" in current_state[row][col]:
                    total += 330 + BISHOP[row][col]
                elif "R" in current_state[row][col]:
                    total += 500 + ROOK[row][col]
                elif "Q" in current_state[row][col]:
                    total += 900 + QUEEN[row][col]
                elif is_endgame(current_state):
                    total += 20000 + KING_END[row][col]
                else:
                    total += 20000 + KING_MID[row][col]
            else:
                if "P" in current_state[row][col]:
                    total -= 100 + PAWN[7 - row][7 - col]
                elif "N" in current_state[row][col]:
                    total -= 320 + KNIGHT[7 - row][7 - col]
                elif "B" in current_state[row][col]:
                    total -= 330 + BISHOP[7 - row][7 - col]
                elif "R" in current_state[row][col]:
                    total -= 500 + ROOK[7 - row][7 - col]
                elif "Q" in current_state[row][col]:
                    total -= 900 + QUEEN[7 - row][7 - col]
                elif is_endgame(current_state):
                    total -= 20000 + KING_END[7 - row][7 - col]
                else:
                    total -= 20000 + KING_MID[7 - row][7 - col]
    return total


# Description: If the input state is in the end game, return True, return False otherwise.
# Pre-condition: current_state is a legal board state of chess.
# Post-condition: Return True if both sides have no queens.
#                 Return True if every side with a queen has no other major pieces and at most 1 minor piece.
#                 Return False otherwise.
def is_endgame(current_state):
    w_queen = (-1, -1)
    b_queen = (-1, -1)
    w_major_piece = True
    b_major_piece = True
    b_minor_pieces = 0
    w_minor_pieces = 0
    for row in range(board_size):
        for col in range(board_size):
            if current_state[row][col] == "wQ" and w_queen == (-1, -1):
                w_queen = (row, col)
            elif current_state[row][col] == "bQ" and b_queen == (-1, -1):
                b_queen = (row, col)
            elif (current_state[row][col] == "wQ" and w_queen != (-1, -1)) or \
                 (current_state[row][col] == "bQ" and b_queen != (-1, -1)) or "R" in current_state[row][col]:
                if "w" in current_state[row][col]:
                    w_major_piece = False
                else:
                    b_major_piece = False
            elif "B" in current_state[row][col] or "N" in current_state[row][col]:
                if "w" in current_state[row][col]:
                    w_minor_pieces += 1
                else:
                    b_minor_pieces += 1
    return (w_queen == b_queen) or (w_queen != (-1, -1) and w_minor_pieces < 2 and w_major_piece) or \
           (b_queen != (-1, -1) and b_minor_pieces < 2 and b_major_piece)


# Description:    Flattens the input list.
# Pre-condition:  the_list is a 2d list (a list of 1d lists).
# Post-condition: the_list is flattened; that is, returned as a 1d list such that its ordering will never vary.
def flatten(the_list):
    flat = []
    for x in the_list:
        for y in x:
            flat.append(y)
    return flat


# Description:    Unflattens the input list.
# Pre-condition:  the_list is a 1d list that had been previously flattened.
# Post-condition: Converts the_list back to its unflattened state.
def unflatten(the_list):
    unflat = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
              ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
              ["--", "--", "--", "--", "--", "--", "--", "--"],
              ["--", "--", "--", "--", "--", "--", "--", "--"],
              ["--", "--", "--", "--", "--", "--", "--", "--"],
              ["--", "--", "--", "--", "--", "--", "--", "--"],
              ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
              ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
    count = 0
    for row in range(board_size):
        for col in range(board_size):
            unflat[row][col] = the_list[count]
            count += 1
    return unflat


# Description:    Returns number of instances of a certain element in a list.
# Pre-condition:  the_list is an n-dimensional list and element is a potential element of the_list.
# Post-condition: The number of instances that element has in the_list is returned.
def num_of_duplicates(the_list, element):
    count = 0
    for x in the_list:
        if x == element:
            count += 1
    return count


# Description: Initializes img list; makes it easy to reference image files for each board piece.
def load_img():
    obj = ["bR", "bN", "bB", "bK", "bQ", "bB", "bN", "bR", "bP", "wP", "wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    for o in obj:
        img[o] = pygame.transform.scale(pygame.image.load("media/images/" + o + ".png"), (tile_size, tile_size))
    img["message"] = pygame.transform.scale(pygame.image.load("media/images/message.png"), (height, width))
    img["message_2"] = pygame.transform.scale(pygame.image.load("media/images/message_2.png"), (height, width))


# Description: Draws the board and the pieces. Also highlights the location of the cursor.
def draw(screen):
    colours = [pygame.Color("white"), pygame.Color("skyblue")]
    for row in range(board_size):
        for column in range(board_size):
            if fun_time == 1:
                x = round(((math.sin(time.time()) + 1) / 2 + 0.25) * 200)
                y = round(((math.sin(time.time() * 1.1) + 1) / 2 + 0.15) * 200)
                z = round(((math.sin(time.time() * 1.2) + 1) / 2 + 0.15) * 200)
                colours[1] = pygame.Color(x, y, z)
            elif fun_time == 2:
                colours[1] = pygame.Color("red")
            elif fun_time == 3:
                colours[1] = pygame.Color("blue")
            elif fun_time == 4:
                colours[1] = pygame.Color("green")
            elif fun_time == 5:
                colours[1] = pygame.Color("magenta")
            elif fun_time == 6:
                colours[1] = pygame.Color("orange")
            elif fun_time == 7:
                colours[1] = pygame.Color("purple")
            elif fun_time == 8:
                colours[1] = pygame.Color("yellow")
            elif fun_time == 9:
                colours[1] = pygame.Color("pink")

            colour = colours[(row + column) % 2]
            pygame.draw.rect(screen, colour, pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size))
            if perspective == "w":
                piece = state[row][column]
            else:
                piece = reverse[row][column]
            if piece != "--":
                screen.blit(img[piece], pygame.Rect(column * tile_size, row * tile_size, tile_size, tile_size))

            coordinate = pygame.mouse.get_pos()
            c = coordinate[0] // tile_size
            r = coordinate[1] // tile_size
            pygame.draw.lines(screen, pygame.Color("darkgrey"), True, [(round(c * tile_size), round(r * tile_size)),
                                                                       (round((c + 1) * tile_size),
                                                                        round(r * tile_size)), (
                                                                           round((c + 1) * tile_size),
                                                                           round((r + 1) * tile_size)), (
                                                                           round(c * tile_size),
                                                                           round((r + 1) * tile_size))], 5)


# Description:    Switches the state from one colour's perspective to the other's.
# Pre-condition:  current_state is a board state of chess, taking the perspective of black or white
# Post-condition: current_state is returned but taking the perspective of the other colour.
def transform(current_state):
    switched = copy.deepcopy(current_state)
    for row in range(board_size):
        for col in range(board_size):
            switched[row][col] = current_state[7 - row][7 - col]
    return switched


# Description: Changes the perspective.
def switch_perspective():
    global perspective
    if perspective == "w":
        perspective = "b"
    else:
        perspective = "w"


# Description:    Indicates if a move is legal or not.
# Pre-condition:  clicks is an array of 2 tuples.
# Post-condition: Returns True if clicks array corresponds to a valid move, False otherwise.
# Example input:  clicks = [(0,0),(1,1)]. The function will be true iff a movement from (0,0) to (1,1) is valid.
def valid_move(clicks):
    from_tile = clicks[0]
    to_tile = clicks[1]
    colour = state[from_tile[0]][from_tile[1]][0]
    if [from_tile, to_tile] in available_moves(colour, state, unflatten(all_states[len(all_states) - 2]), castle):
        return True
    return False


# Description:    Outputs all the legal moves in a position for a colour.
# Pre-condition:  Colour is either "b" for black or "w" for white
#                 current_state is the board state for which we want to generate all legal moves
#                 previous_state is the board state immediately before current_state
#                 castling is an array of four booleans
# Post-condition: All legal moves for the colour are returned.
def available_moves(colour, current_state, previous_state, castling):
    moves = []
    for row in range(board_size):
        for col in range(board_size):
            piece = current_state[row][col]
            if piece == colour + "K":
                register_move(piece, row, -1, col, -1, moves, current_state, previous_state)
                register_move(piece, row, -1, col, 0, moves, current_state, previous_state)
                register_move(piece, row, 0, col, -1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, 1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, 0, moves, current_state, previous_state)
                register_move(piece, row, 0, col, 1, moves, current_state, previous_state)
                register_move(piece, row, -1, col, 1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, -1, moves, current_state, previous_state)
                if colour == "w":
                    if castling[0] and current_state[7][5] == "--" and current_state[7][6] == "--" and \
                       current_state[7][7] == "wR" and (row, col) == (7, 4) and king_safe(current_state, "w"):
                        potential_state = copy.deepcopy(current_state)
                        potential_state[7][4] = "--"
                        potential_state[7][7] = "--"
                        potential_state[7][6] = "wK"
                        potential_state[7][5] = "wR"
                        if king_safe(potential_state, colour):
                            moves.append([(7, 4), (7, 6)])
                    if castling[1] and current_state[7][1] == "--" and current_state[7][2] == "--" and \
                       current_state[7][3] == "--" and current_state[7][0] == "wR" and (row, col) == (7, 4) and \
                       king_safe(current_state, "w"):
                        potential_state = copy.deepcopy(current_state)
                        potential_state[7][4] = "--"
                        potential_state[7][0] = "--"
                        potential_state[7][2] = "wK"
                        potential_state[7][3] = "wR"
                        if king_safe(potential_state, colour):
                            moves.append([(7, 4), (7, 2)])
                else:
                    if castling[2] and current_state[0][5] == "--" and current_state[0][6] == "--" and \
                       current_state[0][7] == "bR" and (row, col) == (0, 4) and king_safe(current_state, "b"):
                        potential_state = copy.deepcopy(current_state)
                        potential_state[0][4] = "--"
                        potential_state[0][7] = "--"
                        potential_state[0][6] = "bK"
                        potential_state[0][5] = "bR"
                        if king_safe(potential_state, colour):
                            moves.append([(0, 4), (0, 6)])
                    if castling[3] and current_state[0][1] == "--" and current_state[0][2] == "--" and \
                       current_state[0][3] == "--" and current_state[0][0] == "bR" and (row, col) == (0, 4) and \
                       king_safe(current_state, "b"):
                        potential_state = copy.deepcopy(current_state)
                        potential_state[0][4] = "--"
                        potential_state[0][0] = "--"
                        potential_state[0][2] = "bK"
                        potential_state[0][3] = "bR"
                        if king_safe(potential_state, colour):
                            moves.append([(0, 4), (0, 2)])
            elif piece == colour + "Q":
                register_move(piece, row, -1, col, -1, moves, current_state, previous_state)
                register_move(piece, row, -1, col, 0, moves, current_state, previous_state)
                register_move(piece, row, 0, col, -1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, 1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, 0, moves, current_state, previous_state)
                register_move(piece, row, 0, col, 1, moves, current_state, previous_state)
                register_move(piece, row, -1, col, 1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, -1, moves, current_state, previous_state)
            elif piece == colour + "R":
                register_move(piece, row, -1, col, 0, moves, current_state, previous_state)
                register_move(piece, row, 1, col, 0, moves, current_state, previous_state)
                register_move(piece, row, 0, col, -1, moves, current_state, previous_state)
                register_move(piece, row, 0, col, 1, moves, current_state, previous_state)
            elif piece == colour + "B":
                register_move(piece, row, -1, col, -1, moves, current_state, previous_state)
                register_move(piece, row, -1, col, 1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, 1, moves, current_state, previous_state)
                register_move(piece, row, 1, col, -1, moves, current_state, previous_state)
            elif piece == colour + "N":
                register_move(piece, row, 0, col, 0, moves, current_state, previous_state)
            elif piece == colour + "P":
                register_move(piece, row, 0, col, 0, moves, current_state, previous_state)
    return moves


# Description: This function is used in the available_moves() function.
def register_move(piece, row, row_val, col, col_val, moves, current_state, previous_state):
    try:
        if piece[0] not in current_state[row + row_val][col + col_val] and (row_val, col_val) != (0, 0):
            if row + row_val < 0 or col + col_val < 0:
                current_state[99][99] = "This will cause an index error!"
            potential_state = copy.deepcopy(current_state)
            potential_state[row][col] = "--"
            potential_state[row + row_val][col + col_val] = piece
            if king_safe(potential_state, piece[0]):
                moves.append([(row, col), (row + row_val, col + col_val)])
        if "Q" in piece or "B" in piece or "R" in piece:
            if row + row_val < 0 or col + col_val < 0:
                current_state[99][99] = "This will cause an index error!"
            while current_state[row + row_val][col + col_val] == "--":
                if row_val < 0:
                    row_val -= 1
                elif row_val > 0:
                    row_val += 1
                if col_val < 0:
                    col_val -= 1
                elif col_val > 0:
                    col_val += 1
                if row + row_val < 0 or col + col_val < 0:
                    current_state[99][99] = "This will cause an index error!"
                potential_state = copy.deepcopy(current_state)
                potential_state[row][col] = "--"
                potential_state[row + row_val][col + col_val] = piece
                if king_safe(potential_state, piece[0]) and piece[0] not in current_state[row + row_val][col + col_val]:
                    moves.append([(row, col), (row + row_val, col + col_val)])
        elif "N" in piece:
            possible = [(row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2),
                        (row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1)]
            for i in range(8):
                try:
                    if possible[i][0] < 0 or possible[i][1] < 0:
                        current_state[99][99] = "This will cause an index error!"
                    potential_state = copy.deepcopy(current_state)
                    potential_state[row][col] = "--"
                    potential_state[possible[i][0]][possible[i][1]] = piece
                    if king_safe(potential_state, piece[0]) and piece[0] not in \
                       current_state[possible[i][0]][possible[i][1]]:
                        moves.append([(row, col), (possible[i][0], possible[i][1])])
                except IndexError:
                    pass
        elif "P" in piece:
            try:
                if piece[0] == "w":
                    one_move = -1
                    two_move = -2
                    pawn_row = 6
                    if row + one_move < 0:
                        current_state[99][99] = "This will cause an index error!"
                else:
                    one_move = 1
                    two_move = 2
                    pawn_row = 1
                if current_state[row + one_move][col] == "--":
                    potential_state = copy.deepcopy(current_state)
                    potential_state[row][col] = "--"
                    potential_state[row + one_move][col] = piece
                    if king_safe(potential_state, piece[0]):
                        moves.append([(row, col), (row + one_move, col)])
                    if current_state[row + two_move][col] == "--" and row == pawn_row:
                        potential_state = copy.deepcopy(current_state)
                        potential_state[row][col] = "--"
                        potential_state[row + two_move][col] = piece
                        if king_safe(potential_state, piece[0]):
                            moves.append([(row, col), (row + two_move, col)])
            except IndexError:
                pass

            try:
                if piece[0] == "w":
                    row_val = -1
                else:
                    row_val = 1
                col_val = -1
                if row + row_val < 0 or col + col_val < 0:
                    current_state[99][99] = "This will cause an index error!"
                if piece[0] not in current_state[row + row_val][col + col_val] and \
                   current_state[row + row_val][col + col_val] != "--":
                    potential_state = copy.deepcopy(current_state)
                    potential_state[row][col] = "--"
                    potential_state[row + row_val][col + col_val] = piece
                    if king_safe(potential_state, piece[0]):
                        moves.append([(row, col), (row + row_val, col + col_val)])
            except IndexError:
                pass

            try:
                if piece[0] == "w":
                    row_val = -1
                    if row + row_val < 0:
                        current_state[99][99] = "This will cause an index error!"
                else:
                    row_val = 1
                col_val = 1
                if piece[0] not in current_state[row + row_val][col + col_val] and \
                   current_state[row + row_val][col + col_val] != "--":
                    potential_state = copy.deepcopy(current_state)
                    potential_state[row][col] = "--"
                    potential_state[row + row_val][col + col_val] = piece
                    if king_safe(potential_state, piece[0]):
                        moves.append([(row, col), (row + row_val, col + col_val)])
            except IndexError:
                pass

            try:
                if piece[0] == "w":
                    if col - 1 < 0 or row - 2 < 0:
                        current_state[99][99] = "This will cause an index error!"
                    if current_state[row][col - 1] == "bP" and previous_state[row - 2][col - 1] == "bP":
                        if current_state[row - 2][col - 1] == "--" and current_state[row - 1][col - 1] == "--":
                            potential_state = copy.deepcopy(current_state)
                            potential_state[row][col] = "--"
                            potential_state[row - 1][col - 1] = piece
                            if king_safe(potential_state, piece[0]):
                                moves.append([(row, col), (row - 1, col - 1)])
                else:
                    if col - 1 < 0:
                        current_state[99][99] = "This will cause an index error!"
                    if current_state[row][col - 1] == "wP" and previous_state[row + 2][col - 1] == "wP":
                        if current_state[row + 2][col - 1] == "--" and current_state[row + 1][col - 1] == "--":
                            potential_state = copy.deepcopy(current_state)
                            potential_state[row][col] = "--"
                            potential_state[row + 1][col - 1] = piece
                            if king_safe(potential_state, piece[0]):
                                moves.append([(row, col), (row + 1, col - 1)])
            except IndexError:
                pass

            try:
                if piece[0] == "w":
                    if row - 2 < 0:
                        current_state[99][99] = "This will cause an index error!"
                    if current_state[row][col + 1] == "bP" and previous_state[row - 2][col + 1] == "bP":
                        if current_state[row - 2][col + 1] == "--" and current_state[row - 1][col + 1] == "--":
                            potential_state = copy.deepcopy(state)
                            potential_state[row][col] = "--"
                            potential_state[row - 1][col + 1] = piece
                            if king_safe(potential_state, piece[0]):
                                moves.append([(row, col), (row - 1, col + 1)])
                else:
                    if current_state[row][col + 1] == "wP" and previous_state[row + 2][col + 1] == "wP":
                        if current_state[row + 2][col + 1] == "--" and current_state[row + 1][col + 1] == "--":
                            potential_state = copy.deepcopy(current_state)
                            potential_state[row][col] = "--"
                            potential_state[row + 1][col + 1] = piece
                            if king_safe(potential_state, piece[0]):
                                moves.append([(row, col), (row + 1, col + 1)])
            except IndexError:
                pass
    except IndexError:
        return


# Description:    Outputs whether or not a player in a given state is in check
# Pre-condition:  potential_state is a board state and colour is "w" if white just ended their turn, "b" otherwise.
# Post-condition: Returns False if the king of a given colour is in check in the potential_state, True otherwise.
def king_safe(potential_state, colour):
    row = 0
    col = 0
    for i in range(8):
        for j in range(8):
            if potential_state[i][j] == colour + "K":
                row = i
                col = j

    if not king_safe_partition(potential_state, row, col, -1, -1, "Q", "B", colour):
        return False
    if not king_safe_partition(potential_state, row, col, 1, 1, "Q", "B", colour):
        return False
    if not king_safe_partition(potential_state, row, col, -1, 1, "Q", "B", colour):
        return False
    if not king_safe_partition(potential_state, row, col, 1, -1, "Q", "B", colour):
        return False
    if not king_safe_partition(potential_state, row, col, 1, 0, "Q", "R", colour):
        return False
    if not king_safe_partition(potential_state, row, col, -1, 0, "Q", "R", colour):
        return False
    if not king_safe_partition(potential_state, row, col, 0, 1, "Q", "R", colour):
        return False
    if not king_safe_partition(potential_state, row, col, 0, -1, "Q", "R", colour):
        return False
    if colour == "w":
        other_colour = "b"
        try:
            if row - 1 < 0 or col - 1 < 0:
                potential_state[99][99] = "This will cause an index error!"
            if potential_state[row - 1][col - 1] == "bP":
                return False
        except IndexError:
            pass
        try:
            if row - 1 < 0:
                potential_state[99][99] = "This will cause an index error!"
            if potential_state[row - 1][col + 1] == "bP":
                return False
        except IndexError:
            pass
    else:
        other_colour = "w"
        try:
            if col - 1 < 0:
                potential_state[99][99] = "This will cause an index error!"
            if potential_state[row + 1][col - 1] == "wP":
                return False
        except IndexError:
            pass
        try:
            if potential_state[row + 1][col + 1] == "wP":
                return False
        except IndexError:
            pass
    possible = [(row + 1, col + 2), (row + 1, col - 2), (row - 1, col + 2), (row - 1, col - 2),
                (row + 2, col + 1), (row + 2, col - 1), (row - 2, col + 1), (row - 2, col - 1)]
    for i in range(8):
        try:
            if possible[i][0] < 0 or possible[i][1] < 0:
                potential_state[99][99] = "This will cause an index error!"
            if potential_state[possible[i][0]][possible[i][1]] == other_colour + "N":
                return False
        except IndexError:
            pass
    try:
        if potential_state[row][col + 1] == other_colour + "K":
            return False
        if potential_state[row + 1][col + 1] == other_colour + "K":
            return False
    except IndexError:
        pass
    try:
        if potential_state[row + 1][col] == other_colour + "K":
            return False
    except IndexError:
        pass
    try:
        if row - 1 < 0 or col - 1 < 0:
            potential_state[99][99] = "This will cause an index error!"
        if potential_state[row - 1][col - 1] == other_colour + "K":
            return False
    except IndexError:
        pass
    try:
        if row - 1 < 0:
            potential_state[99][99] = "This will cause an index error!"
        if potential_state[row - 1][col] == other_colour + "K":
            return False
        if potential_state[row - 1][col + 1] == other_colour + "K":
            return False
    except IndexError:
        pass
    try:
        if col - 1 < 0:
            potential_state[99][99] = "This will cause an index error!"
        if potential_state[row][col - 1] == other_colour + "K":
            return False
        if potential_state[row + 1][col - 1] == other_colour + "K":
            return False
    except IndexError:
        pass
    return True


# Description: This function is used in the king_safe() function.
def king_safe_partition(potential_state, row, col, row_val, col_val, p1, p2, colour):
    try:
        while True:
            if row + row_val < 0 or col + col_val < 0:
                potential_state[99][99] = "This will cause an index error!"
            piece = potential_state[row + row_val][col + col_val]
            if piece[0] != colour and (p1 in piece or p2 in piece):
                return False
            elif piece != "--":
                potential_state[99][99] = "This will cause an index error!"
            row += row_val
            col += col_val
    except IndexError:
        return True


# Description:    Maintains the correctness of the castle global variable when called.
# Pre-condition:  clicks is an array of 2 tuples.
# Post-condition: If the clicks correspond to a move that disables certain castling moves, those changes are reflected.
def castle_enforcement(clicks):
    if castle[0] or castle[1] or castle[2] or castle[3]:
        if clicks[0] == (0, 4):
            castle[2] = False
            castle[3] = False
        elif clicks[0] == (7, 4):
            castle[0] = False
            castle[1] = False
        elif clicks[0] == (0, 0):
            castle[3] = False
        elif clicks[0] == (0, 7):
            castle[2] = False
        elif clicks[0] == (7, 0):
            castle[1] = False
        elif clicks[0] == (7, 7):
            castle[0] = False


# Description: Manages end conditions, piece movement, sound effects, and visual effects.
def main():
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    load_img()
    not_done = True
    tile_selected = ()
    clicks = []
    turn = "w"
    promote = (-1, -1)
    bootleg = False
    closed = False
    last_undo = 0
    time_start = math.inf
    global mode
    global state
    global reverse
    global fifty_move_rule_counter
    if random.randint(0, 1) == 0 and mode == 0:
        switch_perspective()
    if perspective == "b":
        comp_colour = "w"
    else:
        comp_colour = "b"
    all_states.append(flatten(state))
    while not_done:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if (keys[pygame.K_c] or keys[pygame.K_p]) and not closed:
                closed = True
                time_start = min(time_start, time.time())
                if keys[pygame.K_c] and not keys[pygame.K_p]:
                    mode = 0
            if event.type == pygame.QUIT:
                exit(0)
            elif (event.type == pygame.MOUSEBUTTONDOWN or (comp_colour == turn and mode == 0)) and closed:
                if comp_colour == turn and mode == 0:
                    num_of_states = len(all_states)
                    if num_of_states < 2:
                        previous_state = copy.deepcopy(state)
                    else:
                        previous_state = unflatten(all_states[num_of_states - 2])
                    computer = mini_max(copy.deepcopy(state), previous_state, 2, -math.inf, math.inf, comp_colour, castle)
                    state = copy.deepcopy(make_move(state, computer[1], castle)[0])
                    reverse = transform(state)

                    castle_enforcement(computer[1])
                    if turn == "w":
                        turn = "b"
                    else:
                        turn = "w"
                    available = available_moves(turn, state, unflatten(all_states[len(all_states) - 2]), castle)
                    if all_states[len(all_states) - 1] != flatten(state):
                        all_states.append(flatten(state))
                    if not available and king_safe(state, turn):
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/tie.wav"))
                        print("Draw by stalemate: A player has no legal move and their king is not in check.")
                        not_done = False
                    elif not available:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/win.wav"))
                        if turn == "b":
                            print("Black is checkmated. White wins!")
                        else:
                            print("White is checkmated. Black wins!")
                        not_done = False
                    elif num_of_duplicates(all_states, flatten(state)) >= 3:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/tie.wav"))
                        print("Draw by repetition: The same board state was reached three times.")
                        not_done = False
                    elif fifty_move_rule_counter >= 50:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/tie.wav"))
                        print("Draw by the 50-move rule: No captures or pawn moves in 50 consecutive moves.")
                        not_done = False
                elif event.button == 1:
                    coordinate = pygame.mouse.get_pos()
                    column = coordinate[0] // tile_size
                    row = coordinate[1] // tile_size
                    if perspective == "b":
                        row = 7 - row
                        column = 7 - column
                    if tile_selected == (row, column) or (len(clicks) == 0 and turn not in state[row][column]):
                        if tile_selected != (row, column) and state[row][column] != "--":
                            pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/error.wav"))
                        tile_selected = ()
                        clicks = []
                    else:
                        tile_selected = (row, column)
                        clicks.append(tile_selected)
                    if len(clicks) == 2:
                        if valid_move(clicks):
                            if state[clicks[0][0]][clicks[0][1]][0] == "w":
                                other = "b"
                            else:
                                other = "w"
                            potential_state = copy.deepcopy(state)
                            potential_state[clicks[1][0]][clicks[1][1]] = potential_state[clicks[0][0]][clicks[0][1]]
                            potential_state[clicks[0][0]][clicks[0][1]] = "--"
                            if state[clicks[1][0]][clicks[1][1]] != "--" or "P" in state[clicks[0][0]][clicks[0][1]]:
                                fifty_move_rule_counter = 0
                            else:
                                fifty_move_rule_counter += 1
                            if not king_safe(potential_state, other):
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/check.wav"))
                            elif state[clicks[1][0]][clicks[1][1]] == "--":
                                if state[clicks[0][0]][clicks[0][1]] == "wP":
                                    if clicks[1] == (clicks[0][0] - 1, clicks[0][1] + 1) or clicks[1] == (
                                            clicks[0][0] - 1, clicks[0][1] - 1):
                                        state[clicks[1][0] + 1][clicks[1][1]] = "--"
                                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/capture.wav"))
                                    else:
                                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/move.wav"))
                                elif state[clicks[0][0]][clicks[0][1]] == "bP":
                                    if clicks[1] == (clicks[0][0] + 1, clicks[0][1] + 1) or clicks[1] == (
                                            clicks[0][0] + 1, clicks[0][1] - 1):
                                        state[clicks[1][0] - 1][clicks[1][1]] = "--"
                                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/capture.wav"))
                                    else:
                                        pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/move.wav"))
                                elif "K" in state[clicks[0][0]][clicks[0][1]] and math.fabs(
                                        clicks[1][1] - clicks[0][1]) == 2:
                                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/castle.wav"))
                                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("media/sounds/move.wav"))
                                    if state[clicks[0][0]][clicks[0][1]] == "bK":
                                        if clicks[1] == (0, 6):
                                            state[0][7] = "--"
                                            state[0][5] = "bR"
                                        else:
                                            state[0][0] = "--"
                                            state[0][3] = "bR"
                                    else:
                                        if clicks[1] == (7, 6):
                                            state[7][7] = "--"
                                            state[7][5] = "wR"
                                        else:
                                            state[7][0] = "--"
                                            state[7][3] = "wR"
                                else:
                                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/move.wav"))
                            elif state[clicks[1][0]][clicks[1][1]] != "--":
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/capture.wav"))
                            state[clicks[1][0]][clicks[1][1]] = state[clicks[0][0]][clicks[0][1]]
                            state[clicks[0][0]][clicks[0][1]] = "--"
                            if state[0][clicks[1][1]] == "wP" and clicks[1][0] == 0:
                                state[0][clicks[1][1]] = "wQ"
                                promote = (0, clicks[1][1])
                            elif state[7][clicks[1][1]] == "bP" and clicks[1][0] == 7:
                                state[7][clicks[1][1]] = "bQ"
                                promote = (7, clicks[1][1])
                            if promote != (-1, -1):
                                r = promote[0]
                                c = promote[1]
                                index = 0
                                while promote != (-1, -1):
                                    options = ["Q", "N", "R", "B"]
                                    for event_1 in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            exit(0)
                                        elif event_1.type == pygame.MOUSEBUTTONDOWN:
                                            if event_1.button == 4:
                                                index = (index - 1) % 4
                                            elif event_1.button == 5:
                                                index = (index + 1) % 4
                                            elif event_1.button == 1:
                                                promote = (-1, -1)
                                                if mode == 1:
                                                    switch_perspective()
                                        elif event_1.type == pygame.KEYDOWN:
                                            if event_1.key == pygame.K_TAB:
                                                index = (index + 1) % 4
                                            elif event_1.key == pygame.K_RETURN:
                                                promote = (-1, -1)
                                                if mode == 1:
                                                    switch_perspective()
                                        state[r][c] = state[r][c][0] + options[index]
                                        reverse = transform(state)
                                    draw(screen)
                                    if perspective == "w":
                                        pygame.draw.lines(screen, pygame.Color("blue"), True,
                                                          [(round(c * tile_size), round(r * tile_size)),
                                                           (round((c + 1) * tile_size),
                                                            round(r * tile_size)), (
                                                               round((c + 1) * tile_size),
                                                               round((r + 1) * tile_size)), (
                                                               round(c * tile_size),
                                                               round((r + 1) * tile_size))], 5)
                                    else:
                                        pygame.draw.lines(screen, pygame.Color("blue"), True,
                                                          [(round((7 - c) * tile_size), round((7 - r) * tile_size)),
                                                           (round(((7 - c) + 1) * tile_size),
                                                            round((7 - r) * tile_size)), (
                                                               round(((7 - c) + 1) * tile_size),
                                                               round(((7 - r) + 1) * tile_size)), (
                                                               round((7 - c) * tile_size),
                                                               round(((7 - r) + 1) * tile_size))], 5)
                                    clock.tick(fps)
                                    pygame.display.flip()
                            elif mode == 1:
                                switch_perspective()
                            castle_enforcement(clicks)
                            if turn == "w":
                                turn = "b"
                            else:
                                turn = "w"
                            available = available_moves(turn, state, unflatten(all_states[len(all_states) - 2]), castle)
                            if all_states[len(all_states) - 1] != flatten(state):
                                all_states.append(flatten(state))
                            reverse = transform(state)
                            if not available and king_safe(state, turn):
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/tie.wav"))
                                print("Draw by stalemate: A player has no legal move and their king is not in check.")
                                not_done = False
                            elif not available:
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/win.wav"))
                                if turn == "b":
                                    print("Black is checkmated. White wins!")
                                else:
                                    print("White is checkmated. Black wins!")
                                not_done = False
                            elif num_of_duplicates(all_states, flatten(state)) >= 3:
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/tie.wav"))
                                print("Draw by repetition: The same board state was reached three times.")
                                not_done = False
                            elif fifty_move_rule_counter >= 50:
                                pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/tie.wav"))
                                print("Draw by the 50-move rule: No captures or pawn moves in 50 consecutive moves.")
                                not_done = False
                        else:
                            if state[clicks[0][0]][clicks[0][1]][0] in state[clicks[1][0]][clicks[1][1]]:
                                bootleg = True
                                tile_selected = (clicks[1][0], clicks[1][1])
                                clicks = [tile_selected]
                        if not bootleg:
                            clicks = []
                            tile_selected = ()
                        else:
                            bootleg = False
            elif event.type == pygame.KEYDOWN and closed:
                global fun_time
                if event.key == pygame.K_1:
                    fun_time = 1
                elif event.key == pygame.K_2:
                    fun_time = 2
                elif event.key == pygame.K_3:
                    fun_time = 3
                elif event.key == pygame.K_4:
                    fun_time = 4
                elif event.key == pygame.K_5:
                    fun_time = 5
                elif event.key == pygame.K_6:
                    fun_time = 6
                elif event.key == pygame.K_7:
                    fun_time = 7
                elif event.key == pygame.K_8:
                    fun_time = 8
                elif event.key == pygame.K_9:
                    fun_time = 9
                elif event.key == pygame.K_0:
                    fun_time = 0
            elif keys[pygame.K_LCTRL] and keys[pygame.K_z] and time.time() - last_undo >= 0.2 and closed:
                try:
                    if len(all_states) < 2 and mode == 1 or (len(all_states) < 3 and mode == 0):
                        state[99][99] = "This will cause an index error!"
                    if mode == 0:
                        state = copy.deepcopy(unflatten(all_states[len(all_states) - 3]))
                        all_states.pop()
                        all_states.pop()
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                    elif mode == 1:
                        state = copy.deepcopy(unflatten(all_states[len(all_states) - 2]))
                        reverse = transform(state)
                        all_states.pop()
                        if turn == "w":
                            turn = "b"
                        else:
                            turn = "w"
                        switch_perspective()
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/move.wav"))
                    last_undo = time.time()
                except IndexError:
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("media/sounds/error.wav"))
            elif keys[pygame.K_f] and closed and time.time() - 1 >= time_start and time.time() - last_undo >= 0.2:
                switch_perspective()
                last_undo = time.time()
        if closed:
            draw(screen)
        else:
            if math.floor(time.time()*1.25) % 2 == 0:
                screen.blit(img["message"], pygame.Rect(0, 0, height, width))
            else:
                screen.blit(img["message_2"], pygame.Rect(0, 0, height, width))
        if len(clicks) == 1:
            if turn in state[clicks[0][0]][clicks[0][1]]:
                row = clicks[0][0]
                col = clicks[0][1]
                if perspective == "b":
                    row = 7 - row
                    col = 7 - col
                pygame.draw.lines(screen, pygame.Color("darkgrey"), True,
                                  [(round(col * tile_size), round(row * tile_size)),
                                   (round((col + 1) * tile_size), round(row * tile_size)),
                                   (round((col + 1) * tile_size), round((row + 1) * tile_size)),
                                   (round(col * tile_size), round((row + 1) * tile_size))], 5)
                legal_moves = []
                for move in available_moves(turn, state, unflatten(all_states[len(all_states) - 2]), castle):
                    if move[0] == clicks[0]:
                        legal_moves.append(move[1])
                for move in legal_moves:
                    row = move[0]
                    col = move[1]
                    if perspective == "b":
                        row = 7 - row
                        col = 7 - col
                    pygame.draw.circle(screen, pygame.Color("darkgrey"),
                                       (round((col + 0.5) * tile_size), round((row + 0.5) * tile_size)), tile_size // 8)
        if not king_safe(state, turn):
            row = 0
            col = 0
            for i in range(8):
                for j in range(8):
                    if state[i][j] == turn + "K":
                        row = i
                        col = j
            if perspective == "b":
                row = 7 - row
                col = 7 - col
            pygame.draw.lines(screen, pygame.Color("red"), True, [(round(col * tile_size), round(row * tile_size)),
                                                                  (round((col + 1) * tile_size),
                                                                   round(row * tile_size)), (
                                                                      round((col + 1) * tile_size),
                                                                      round((row + 1) * tile_size)), (
                                                                      round(col * tile_size),
                                                                      round((row + 1) * tile_size))], 5)
        clock.tick(fps)
        pygame.display.flip()
        if not not_done:
            time.sleep(3)


# If this file were to be imported, these two lines make it so that the program would not immediately run.
if __name__ == "__main__":
    main()
