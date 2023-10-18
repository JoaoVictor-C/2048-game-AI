from numba import njit
import numpy.random as random

@njit(fastmath=True)
def add_random_num(matrix):
    zero_list = [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == 0]
    if len(zero_list) == 0:
        return matrix
    index = random.randint(0, len(zero_list))
    i, j = list(zero_list)[index]
    matrix[i][j] = 1 if random.random() < 0.9 else 2
    return matrix


@njit(fastmath=True)
def move_up(matrix):
    for j in range(4):
        i = 0
        while i < 4:
            if matrix[i][j] == 0:
                i += 1
                continue
            k = i + 1
            while k < 4:
                if matrix[k][j] == 0:
                    k += 1
                    continue
                if matrix[i][j] == matrix[k][j]:
                    matrix[i][j] += 1
                    matrix[k][j] = 0
                break
            i = k
    for j in range(4):
        i = 0
        while i < 4:
            if matrix[i][j] == 0:
                k = i + 1
                while k < 4:
                    if matrix[k][j] == 0:
                        k += 1
                        continue
                    matrix[i][j] = matrix[k][j]
                    matrix[k][j] = 0
                    break
                i += 1
                continue
            i += 1
    return add_random_num(matrix)

@njit(fastmath=True)
def move_down(matrix):
    for j in range(4):
        i = 3
        while i >= 0:
            if matrix[i][j] == 0:
                i -= 1
                continue
            k = i - 1
            while k >= 0:
                if matrix[k][j] == 0:
                    k -= 1
                    continue
                if matrix[i][j] == matrix[k][j]:
                    matrix[i][j] += 1
                    matrix[k][j] = 0
                break
            i = k
    for j in range(4):
        i = 3
        while i >= 0:
            if matrix[i][j] == 0:
                k = i - 1
                while k >= 0:
                    if matrix[k][j] == 0:
                        k -= 1
                        continue
                    matrix[i][j] = matrix[k][j]
                    matrix[k][j] = 0
                    break
                i -= 1
                continue
            i -= 1
    return add_random_num(matrix)

@njit(fastmath=True)
def move_left(matrix):
    for i in range(4):
        j = 0
        while j < 4:
            if matrix[i][j] == 0:
                j += 1
                continue
            k = j + 1
            while k < 4:
                if matrix[i][k] == 0:
                    k += 1
                    continue
                if matrix[i][j] == matrix[i][k]:
                    matrix[i][j] += 1
                    matrix[i][k] = 0
                break
            j = k
    for i in range(4):
        j = 0
        while j < 4:
            if matrix[i][j] == 0:
                k = j + 1
                while k < 4:
                    if matrix[i][k] == 0:
                        k += 1
                        continue
                    matrix[i][j] = matrix[i][k]
                    matrix[i][k] = 0
                    break
                j += 1
                continue
            j += 1
    return add_random_num(matrix)

@njit(fastmath=True)
def move_right(matrix):
    for i in range(4):
        j = 3
        while j >= 0:
            if matrix[i][j] == 0:
                j -= 1
                continue
            k = j - 1
            while k >= 0:
                if matrix[i][k] == 0:
                    k -= 1
                    continue
                if matrix[i][j] == matrix[i][k]:
                    matrix[i][j] += 1
                    matrix[i][k] = 0
                break
            j = k
    for i in range(4):
        j = 3
        while j >= 0:
            if matrix[i][j] == 0:
                k = j - 1
                while k >= 0:
                    if matrix[i][k] == 0:
                        k -= 1
                        continue
                    matrix[i][j] = matrix[i][k]
                    matrix[i][k] = 0
                    break
                j -= 1
                continue
            j -= 1
    return add_random_num(matrix)

@njit(fastmath=True)
def is_game_over(matrix):
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                return False
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1]:
                return False
            if matrix[i][j] == matrix[i + 1][j]:
                return False
    return True