import numpy as np


def print_board(board):
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[7] + '|' + board[8] + '|' + board[9])
    print("\n")


def is_space_available(position):
    return (position in range(1, 10)) and board[position] == ' '


def insert_letter(letter, position):
    if is_space_available(position):
        board[position] = letter
        print_board(board)
        if check_for_draw():
            print("Draw!")
            exit()
        if check_for_win():
            if letter == 'X':
                print("Bot wins!")
                exit()
            else:
                print("Player wins!")
                exit()

    else:
        print("Can't insert there!")
        position = int(input("Please enter new position:  "))
        insert_letter(letter, position)


def check_for_win():
    if board[1] == board[2] and board[1] == board[3] and board[1] != ' ':
        return True
    elif board[4] == board[5] and board[4] == board[6] and board[4] != ' ':
        return True
    elif board[7] == board[8] and board[7] == board[9] and board[7] != ' ':
        return True
    elif board[1] == board[4] and board[1] == board[7] and board[1] != ' ':
        return True
    elif board[2] == board[5] and board[2] == board[8] and board[2] != ' ':
        return True
    elif board[3] == board[6] and board[3] == board[9] and board[3] != ' ':
        return True
    elif board[1] == board[5] and board[1] == board[9] and board[1] != ' ':
        return True
    elif board[7] == board[5] and board[7] == board[3] and board[7] != ' ':
        return True
    else:
        return False


def check_who_won(mark):
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    elif board[4] == board[5] and board[4] == board[6] and board[4] == mark:
        return True
    elif board[7] == board[8] and board[7] == board[9] and board[7] == mark:
        return True
    elif board[1] == board[4] and board[1] == board[7] and board[1] == mark:
        return True
    elif board[2] == board[5] and board[2] == board[8] and board[2] == mark:
        return True
    elif board[3] == board[6] and board[3] == board[9] and board[3] == mark:
        return True
    elif board[1] == board[5] and board[1] == board[9] and board[1] == mark:
        return True
    elif board[7] == board[5] and board[7] == board[3] and board[7] == mark:
        return True
    else:
        return False


def check_for_draw():
    for key in board.keys():
        if board[key] == ' ':
            return False
    return True


def player_move():
    position = int(input("Enter the position for 'O':  "))
    insert_letter(player, position)


def utility_value():
    if check_who_won(bot):
        return 1
    elif check_who_won(player):
        return -1
    elif check_for_draw():
        return 0


def max_value(board, alpha, beta, depth):
    if check_for_draw() or check_for_win():  # Is the game over
        return utility_value()
    else:
        best_score = np.NINF  # best_score représente v dans le pseudo-code minimax
        for move in board.keys():
            if board[move] == ' ':  # The move is possible
                board[move] = bot
                alpha_memory, beta_memory = alpha, beta
                best_score = max(best_score,
                                 min_value(board, alpha, beta, depth=depth+1))
                board[move] = ' '  # Get back to the previous game
                alpha, beta = alpha_memory, beta_memory
                if best_score > beta:
                    return best_score
                alpha = max(alpha, best_score)
        return best_score


def min_value(board, alpha, beta, depth):
    if check_for_draw() or check_for_win():  # Is the game over
        return utility_value()
    else:
        best_score = np.inf  # best_score représente v dans le pseudo-code minimax
        for move in board.keys():
            if board[move] == ' ':  # The move is possible
                board[move] = player
                alpha_memory, beta_memory = alpha, beta
                best_score = min(best_score,
                                 max_value(board, alpha, beta, depth=depth+1))
                alpha, beta = alpha_memory, beta_memory
                board[move] = ' '  # Get back to the previous game
                if best_score < alpha:
                    return best_score
                beta = max(alpha, best_score)
        return best_score


def alpha_beta_search():
    best_score = np.NINF
    best_move = 0
    for move in board.keys():
        if board[move] == ' ':
            board[move] = bot
            score = min_value(board, alpha=np.NINF, beta=np.inf, depth=1)
            board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move

    insert_letter(bot, best_move)


board = {1: ' ', 2: ' ', 3: ' ',
         4: ' ', 5: ' ', 6: ' ',
         7: ' ', 8: ' ', 9: ' '}

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




