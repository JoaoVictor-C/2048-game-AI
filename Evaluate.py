from numba import njit
import numpy as np


# @njit(fastmath=True)
# def evaluate(matrix):
#     evaluation = 0
#     score = 0
#     score += evaluate_score(matrix)
#     evaluation += score
#     return evaluation


@njit(fastmath=True)
def evaluate(matrix):
    score = 0
    for i in range(4):
        for j in range(4):
            if not matrix[i][j] == 0:
                score += np.power(2, matrix[i][j])
    return score


@njit(fastmath=True)
def evaluate_neighbors(matrix):
    evaluation = 0
    neighbors = 0
    for i in range(4):
        row = matrix[i]
        for j in range(1, 4):
            if row[j] == row[j - 1] and row[j] != 0:
                neighbors += 1
    for i in range(4):
        column = [matrix[j][i] for j in range(4)]
        for j in range(1, 4):
            if column[j] == column[j - 1] and column[j] != 0:
                neighbors += 1
    evaluation += neighbors
    return evaluation


@njit(fastmath=True)
def evaluate_monotonicity(matrix):
    evaluation = 0
    monotonicity = 0
    row = [matrix[i][0] for i in range(4)]
    column = [matrix[0][i] for i in range(4)]
    for i in range(1, 4):
        if row[i] >= row[i - 1] and row[i] != 0:
            monotonicity += 1
        elif row[i] <= row[i - 1] and row[i] != 0:
            monotonicity -= 1
        if column[i] >= column[i - 1] and column[i] != 0:
            monotonicity += 1
        elif column[i] <= column[i - 1] and column[i] != 0:
            monotonicity -= 1
    biggest = -1
    for i in range(4):
        for j in range(1, 4):
            if matrix[i][j] > biggest:
                biggest = matrix[i][j]
    corner = [matrix[0][0], matrix[0][3], matrix[3][0], matrix[3][3]]
    if biggest in corner:
        evaluation += 5
    else:
        evaluation -= 1
    evaluation += monotonicity
    return evaluation


@njit(fastmath=True)
def evaluate_smoothness(matrix):
    evaluation = 0
    smoothness = 0
    row = [matrix[i][0] for i in range(4)]
    column = [matrix[0][i] for i in range(4)]
    for i in range(1, 4):
        smoothness += abs(row[i] - row[i - 1])
        smoothness += abs(column[i] - column[i - 1])
    evaluation += smoothness
    return -evaluation


@njit(fastmath=True)
def evaluate_empty_cells(matrix):
    empty_cells = 16 - np.count_nonzero(matrix)
    return empty_cells
