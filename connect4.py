import numpy as np
from termcolor import colored

n_columns, n_lines = 12, 6


def create_board():
    board = {}
    for column in range(1, n_columns + 1):
        board[column] = [' '] * n_lines
    return board


def print_board(board):
    for line in range(n_lines):
        print_line = '|'
        for column in board.keys():
            print_line += f'{board[column][line]}|'
        print(print_line)


def is_column_available(column):
    return (column in range(1, n_columns)) and (' ' in board[column])


def max_line_for_a_new_coin(column):
    depth = 0  # Depth -1 means out f the board
    while board[column][depth] == ' ' and depth < (n_lines):
        depth += 1
    depth -= 1
    return depth


def check_for_draw():
    """Works only after victory was checked"""
    for column in board.keys():
        for line in range(n_lines):
            if board[column][line] == ' ':
                return False
    return True


def check_for_win():
    columns = board.keys()

    for piece in ['X', 'O']:  # For each player

        # Check horizontal locations for win
        for c in range(min(columns), max(columns) - 3):
            for r in range(n_lines):
                if board[c][r] == piece and board[c + 1][r] == piece and\
                        board[c + 2][r] == piece and board[c + 3][r] == piece:
                    return True

        # Check vertical locations for win
        for c in board.keys():
            for r in range(n_lines-3):
                if board[c][r] == piece and board[c][r+1] == piece and\
                        board[c][r + 2] == piece and board[c][r + 3] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(min(columns), max(columns) - 3):
            for r in range(n_lines - 3):
                if board[c][r] == piece and board[c + 1][r + 1] == piece and board[c + 2][r + 2] == piece and \
                        board[c + 3][r + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(min(columns), max(columns) - 3):
            for r in range(3, n_lines):
                if board[c][r] == piece and board[c + 1][r - 1] == piece and board[c + 2][r - 2] == piece and \
                        board[c + 3][r - 3] == piece:
                    return True
    return False


def insert_letter(letter, column):
    if is_column_available(column):
        board[column][max_line_for_a_new_coin(column)] = letter
        print_board(board)
        if check_for_win():
            if letter == 'X':
                print("Bot wins!")
                exit()
            else:
                print("Player wins!")
                exit()
        if check_for_draw():
            print("Draw!")
            exit()

    else:
        print("Can't insert there!")
        column = int(input("Please enter new position:  "))
        insert_letter(letter, column)


board = create_board()
board[1][0] = 3
print_board(board)
print(max_line_for_a_new_coin(1))

print_board(board)
current_player = int(input('Enter who should start\n0 for player\n1 for bot\n'))
print("Positions are as follow:")
print("1, 2, 3\n4, 5, 6\n7, 8, 9\n")

player = 'O'
bot = 'X'

while not check_for_win():
    if current_player == 0:
        player_move()
        current_player = 1
    else:
        alpha_beta_search()
        current_player = 0