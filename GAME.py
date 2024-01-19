# Project: Connect4 w/ AI
# Author: Roel-Junior Alejo Viernes
# Description: Connect 4 game with AI as Player 2


import sys, pygame, math, numpy as np

blue = (0, 0, 255)
black = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 7
COLUMN_COUNT = 7


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
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
turn = 0

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

while not game_over:

    pygame.draw.rect(screen, black, (0, 0, width, square_size))
    pygame.draw.rect(screen, black, (750, 300, 210, 50))

    if turn == 0:
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
                if turn == 0:
                    col = int(math.floor(posx / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True


                # # Ask for Player 2 Input
                else:
                    col = int(math.floor(posx / square_size))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)