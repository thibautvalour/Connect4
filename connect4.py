import numpy as np
import time
from termcolor import colored
import random

n_columns, n_lines = 12, 6

def create_board():
    board = {}
    for column in range(1, n_columns + 1):
        board[column] = ([' '] * n_lines).copy()
    return board


def print_board(board):
    for line in range(n_lines):
        print('|', end='')
        for column in board.keys():
            if board[column][line] == 'X':
                print(colored('X', 'red'), end='')
            elif board[column][line] == 'O':
                print(colored('O', 'blue'), end='')
            else:
                print(' ', end='')
            print('|', end='')
        print('')

    print_line = ' '
    for column in board.keys():
        print_line += f'{column} '
    print(print_line)


def is_column_available(column):
    return (column in list(board.keys())) and (' ' in board[column])


def max_line_for_a_new_coin(column):
    deepest_line = 0  # Depth -1 means out f the board
    while deepest_line < (n_lines) and board[column][deepest_line] == ' ':
        deepest_line += 1
    deepest_line -= 1
    return deepest_line


def check_for_draw(move_count):
    return move_count >= 41


def check_for_win():
    columns = board.keys()

    for mark in [player, bot]:  # For each player

        # Check horizontal locations for win
        for c in range(min(columns), max(columns) - 3):
            for r in range(n_lines):
                try:
                    if board[c][r] == board[c + 1][r] == board[c + 2][r] == board[c + 3][r] == mark:
                        return True
                except:
                    print_board(board)
                    exit()

        # Check vertical locations for win
        for c in board.keys():
            for r in range(n_lines - 3):
                if board[c][r] == board[c][r + 1] == board[c][r + 2] == board[c][r + 3] == mark:
                    return True

        # Check positively sloped diagonals
        for c in range(min(columns), max(columns) - 3):
            for r in range(n_lines - 3):
                if board[c][r] == board[c + 1][r + 1] == board[c + 2][r + 2] == board[c + 3][r + 3] == mark:
                    return True

        # Check negatively sloped diagonals
        for c in range(min(columns), max(columns) - 3):
            for r in range(3, n_lines):
                if board[c][r] == board[c + 1][r - 1] == board[c + 2][r - 2] == board[c + 3][r - 3] == mark:
                    return True
    return False


def check_who_won(mark):
    columns = board.keys()

    # Check horizontal locations for win
    for c in range(min(columns), max(columns) - 3):
        for r in range(n_lines):
            if board[c][r] == board[c + 1][r] == board[c + 2][r] == board[c + 3][r] == mark:
                return True

    # Check vertical locations for win
    for c in board.keys():
        for r in range(n_lines - 3):
            if board[c][r] == board[c][r + 1] == board[c][r + 2] == board[c][r + 3] == mark:
                return True

    # Check positively sloped diagonals
    for c in range(min(columns), max(columns) - 3):
        for r in range(n_lines - 3):
            if board[c][r] == board[c + 1][r + 1] == board[c + 2][r + 2] == board[c + 3][r + 3] == mark:
                return True

    # Check negatively sloped diagonals
    for c in range(min(columns), max(columns) - 3):
        for r in range(3, n_lines):
            if board[c][r] == board[c + 1][r - 1] == board[c + 2][r - 2] == board[c + 3][r - 3] == mark:
                return True
    return False


def insert_letter(letter, column, total_time_AI, move_count):
    if is_column_available(column):
        board[column][max_line_for_a_new_coin(column)] = letter
        print_board(board)
        if check_for_win():
            if letter == 'X':
                print(f"Bot wins! \n Total computing time for AI {round(total_time_AI, 3)} seconds")
                exit()
            else:
                print(f"Player wins! \n Total computing time for AI {round(total_time_AI, 3)} second")
                exit()
        if check_for_draw(move_count):
            print(f"Draw! \n Total computing time for AI {round(total_time_AI, 3)} second")
            exit()

    else:
        if letter == 'X':
            alpha_beta_search(total_time_AI)
        else:
            print("Can't insert there!")
            column = int(input("Please enter new position:  "))
            insert_letter(letter, column, total_time_AI, move_count)


def player_move(total_time_for_AI, move_count):
    good_format = False
    while not good_format:
        column = input("Enter the position for 'O':  ")  # Ask column
        good_format = column.isdigit()  # check the format
    column = int(column)
    insert_letter(player, column, total_time_for_AI, move_count)


########## IA ##########

def utility_value_for_game_over(move_count):
    if check_who_won(bot):
        return np.inf
    elif check_who_won(player):
        return np.NINF
    elif check_for_draw(move_count):
        return 0


def utility_value_for_unfinished_game():
    heuristic = 0
    columns = board.keys()

    for c in range(min(columns), max(columns)):
        for r in range(n_lines):

            try:  # Check horizontal locations for win
                if board[c][r] == board[c + 1][r] == player:
                    heuristic -= 10
                elif board[c][r] == board[c + 1][r] == bot:
                    heuristic += 10
            except:
                pass
            try:
                if board[c][r] == board[c + 1][r] == board[c + 2][r] == bot:
                    heuristic += 100
                elif board[c][r] == board[c + 1][r] == board[c + 2][r] == player:
                    heuristic -= 100
            except:
                pass

            try:  # Check vertical locations for win
                if board[c][r] == board[c][r + 1] == bot:
                    heuristic += 10
                elif board[c][r] == board[c][r + 1] == player:
                    heuristic -= 10
            except:
                pass
            try:
                if board[c][r] == board[c][r + 1] == board[c][r + 2] == bot:
                    heuristic += 100
                elif board[c][r] == board[c][r + 1] == board[c][r + 2] == player:
                    heuristic -= 100
            except:
                pass
            try:  # Check positively sloped diagonals
                if board[c][r] == board[c + 1][r + 1] == bot:
                    heuristic += 10
                elif board[c][r] == board[c + 1][r + 1] == player:
                    heuristic -= 10
            except:
                pass
            try:
                if board[c][r] == board[c + 1][r + 1] == board[c + 2][r + 2] == bot:
                    heuristic += 100
                elif board[c][r] == board[c + 1][r + 1] == board[c + 2][r + 2] == player:
                    heuristic -= 100
            except:
                pass

            try:  # Check negatively sloped diagonals
                if board[c][r] == board[c + 1][r - 1] == bot:
                    heuristic += 10
                elif board[c][r] == board[c + 1][r - 1] == player:
                    heuristic -= 10
            except:
                pass
            try:
                if board[c][r] == board[c + 1][r - 1] == board[c + 2][r - 2] == bot:
                    heuristic += 100
                elif board[c][r] == board[c + 1][r - 1] == board[c + 2][r - 2] == player:
                    heuristic -= 100
            except:
                pass

    return heuristic


def max_value(board, alpha, beta, depth, move_count):
    if check_for_draw(move_count) or check_for_win():  # Is the game over
        return utility_value_for_game_over(move_count)

    elif depth == max_exploration_depth:
        return utility_value_for_unfinished_game()

    else:
        best_score = np.NINF  # best_score représente v dans le pseudo-code minimax
        for column in board.keys():
            if is_column_available(column):  # The move is possible

                max_line = max_line_for_a_new_coin(column)
                board[column][max_line] = bot

                best_score = max(best_score,
                                 min_value(board, alpha, beta,
                                           depth=depth + 1, move_count=move_count+1))

                board[column][max_line] = ' '  # Get back to the previous game

                if best_score > beta:
                    return best_score
                alpha = max(alpha, best_score)
        return best_score


def min_value(board, alpha, beta, depth, move_count):
    if check_for_draw(move_count) or check_for_win():  # Is the game over
        return utility_value_for_game_over(move_count)

    elif depth == max_exploration_depth:
        return utility_value_for_unfinished_game()

    else:
        best_score = np.inf  # best_score représente v dans le pseudo-code minimax
        for column in board.keys():
            if is_column_available(column):  # The move is possible

                max_line = max_line_for_a_new_coin(column)
                board[column][max_line] = player

                best_score = min(best_score,
                                 max_value(board, alpha, beta,
                                           depth=depth + 1, move_count=move_count+1))

                board[column][max_line] = ' '  # Get back to the previous game

            if best_score < alpha:
                return best_score
            beta = max(alpha, best_score)
    return best_score


def alpha_beta_search(total_time_AI, move_count):
    print('\nAI is preparing its next move')
    start = time.time()
    best_score = np.NINF
    best_column = random.randint(1, 12)
    for column in board.keys():
        if is_column_available(column):

            max_line = max_line_for_a_new_coin(column)
            board[column][max_line] = bot

            score = min_value(board, alpha=np.NINF, beta=np.inf, depth=1,
                              move_count=move_count)
            board[column][max_line] = ' '
            if score > best_score:
                best_score = score
                best_column = column
    end = time.time()
    print(f'AI played column {best_column} in {round(end - start, 3)} seconds')
    insert_letter(bot, best_column, total_time_AI, move_count)


board = create_board()
print_board(board)

current_player = int(input('Indicate who will start\n0 for player\n1 for bot\n'))
max_exploration_depth = int(input('Indicate level of the AI\nLevel 4 : 3 seconds of computing per move\n\
Level 5 : 40 seconds of computing per move\n'))

player = 'O'
bot = 'X'
total_time_for_AI = 0
first_AI_move = True
move_count = 0

while not check_for_win():

    if current_player == 0:
        player_move(total_time_for_AI, move_count)
        current_player = 1

    else:
        start = time.time()
        if first_AI_move:
            insert_letter(bot, 6, total_time_for_AI, move_count)
            print('AI played column 6 immediately (0.0 second)')
            first_AI_move = False
        else:
            alpha_beta_search(total_time_for_AI, move_count)

        end = time.time()
        total_time_for_AI += end - start
        current_player = 0
    move_count += 1