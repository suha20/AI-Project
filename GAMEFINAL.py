import sys, pygame, math, numpy as np,random



Difficulty_level = int(input("Please insert the difficulty level : "))

blue = (0, 0, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 7
COLUMN_COUNT = 7

EMPTY = 0

player = 0
AI = 1

player_piece = 1
AI_piece = 2

window_length = 4

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece): #defining the winning parameter
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1]  == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True

def evaluate_window(window,piece,score) :
    score = 0

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:  # checks if the one position is empty after the third one
        score += 15
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 10
    if window.count(player_piece) == 3 and window.count(EMPTY) == 1:
        score += -80
    if window.count(player_piece) == 2 and window.count(EMPTY) == 2:
        score += -50

    return score


def get_score(board,piece):
    # SCORE-HORIZONTALLY
    score = 0
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+window_length]

            score += evaluate_window(window,piece,score)

    # SCORE- VERTICALLY
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+window_length]

            score += evaluate_window(window,piece,score)

    # SCORE - POSITIVE DIAGONALLY
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(window_length)]

            score += evaluate_window(window,piece,score)

    # SCORE - NEGATIVE DIAGONALLY
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - 3 + i][c - i] for i in range(window_length)]

            score += evaluate_window(window,piece,score)

    return score

def get_valid_locations(board) :
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board,piece) :
    valid_locations = get_valid_locations(board)
    best_score = 0
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        new_board = board.copy()
        drop_piece(new_board,row,col,piece)
        score = get_score(new_board,piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def is_terminal_node(board) : # returns the value if they're true
    return winning_move(board,AI_piece) or winning_move(board,player_piece) or len(get_valid_locations(board)) == 0


def MINIMAX(board, Difficulty_level,alpha,beta, maximizingplayer):
    valid_locations = get_valid_locations(board)
    terminal_node = is_terminal_node(board)

    if Difficulty_level == 0 or terminal_node:
        if terminal_node:
            if winning_move(board, AI_piece):
                return (None, 10000000000000)
            elif winning_move(board, player_piece):
                return (None,-10000000000)
            else:  # no more valid moves remaining/game over
                return (None,0)
        else: #depth is zero
            return (None,get_score(board,AI_piece))
    if maximizingplayer:
        value = -math.inf
        best_max_column = random.choice(valid_locations)
        for col in valid_locations : #possible moves to make
            row = get_next_open_row(board,col)
            new_board = board.copy()
            drop_piece(new_board,row,col,AI_piece)
            new_value = MINIMAX(new_board,Difficulty_level-1,alpha,beta,False)[1]


            if new_value > value:
                value = new_value
                best_max_column = col
            # alpha-beta pruning
            alpha =max(alpha,value)
            if beta <= alpha :
                break  # prune remaining nodes

        return best_max_column,value

    else: #for minimizing player
        value = +math.inf
        best_min_column = random.choice(valid_locations)
        for col in valid_locations:  # child nodes/possible moves to make
            row = get_next_open_row(board, col)
            new_board = board.copy()
            drop_piece(new_board, row, col, player_piece)
            new_value1 = MINIMAX(new_board, Difficulty_level - 1,alpha,beta, True)[1]

            if new_value1 < value :
                value = new_value1
                best_min_column = col

            beta = min(beta, value)
            if beta <= alpha:
                break # prune remaining nodes
        return best_min_column,value




def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, blue, (c * square_size, r * square_size + square_size, square_size, square_size))
            pygame.draw.circle(screen, black, (
            int(c * square_size + square_size / 2), int(r * square_size + square_size + square_size / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                int(c * square_size + square_size / 2), height - int(r * square_size + square_size / 2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False


# initalize pygame
pygame.init()

# define our screen size
square_size = 100

# define width and height of board
width = COLUMN_COUNT * square_size + 350
height = (ROW_COUNT + 1) * square_size

size = (width, height)

RADIUS = int(square_size / 2 - 5)

screen = pygame.display.set_mode(size)

# Calling function draw_board again
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)
myfont2 = pygame.font.SysFont("Comic Sans MS", 30)
posx = 50

turn = random.randint(player, AI)  # to generate random first turns between player and AI
while not game_over:

    pygame.draw.rect(screen, black, (0, 0, width, square_size))
    pygame.draw.rect(screen, black, (750, 300, 210, 50))

    if turn == player:
        pygame.draw.circle(screen, RED, (posx, int(square_size / 2)), RADIUS)
        label = myfont2.render("Player 1's turn", 1, RED)

    else:
        pygame.draw.circle(screen, YELLOW, (posx, int(square_size / 2)), RADIUS)
        label = myfont2.render("Player 2's turn", 1, YELLOW)

    screen.blit(label, (750, 300))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            """
            if the user quits the game, the game will exit
            """
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                posx = max(posx - square_size, 50)

            elif event.key == pygame.K_l:
                posx = min(posx + square_size, 650)

        pygame.display.update()

        #
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                pygame.draw.rect(screen, black, (0, 0, width, square_size))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == player:
                    col = int(math.floor(posx / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, player_piece)

                        if winning_move(board, player_piece):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        print_board(board)
                        draw_board(board)
                        turn += 1
                        turn = turn % 2


    # # Ask for Player 2 Input
    if turn == AI and not game_over:
        col,max_score = MINIMAX(board, Difficulty_level, -math.inf, math.inf ,True )

        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_piece)  # placing the piece in the board

            if winning_move(board, AI_piece):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            print_board(board)
            draw_board(board)
            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
