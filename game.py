import numpy as np
import time
import math


def is_tictacto_finished_and_who_won(game):
    diagonal_1 = game[0, 0] * game[1, 1] * game[2, 2]
    diagonal_2 = game[2, 0] * game[1, 1] * game[0, 2]

    if diagonal_1 == 1 or diagonal_2 == 1:  # 1 = 1*1*1
        return True, 1
    elif diagonal_1 == 8 or diagonal_2 == 8:  # 8 = 2*2*2
        return True, 2
    else:  # No diagonal win
        for i in range(3):  # Test each column or line win
            line = game[i, 0] * game[i, 1] * game[i, 2]
            column = game[0, i] * game[1, i] * game[2, i]
            if line == 1 or column == 1:
                return True, 1
            elif line == 8 or column == 8:
                return True, 2
        if not (0 in game):
            return True, 0  # Draw
        else:
            return False, 0


game = np.array([[1, 2, 1],
                 [2, 1, 2],
                 [2, 2, 1]])

if __name__ == '__main__':
    print(is_tictacto_finished_and_who_won(game))
