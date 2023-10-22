from numba import njit
import numpy as np

gridSize = 4

@njit(fastmath=True)
def evaluate(matrix):
    powers_of_2 = np.power(2, matrix)
    score = np.sum(powers_of_2) - (gridSize * gridSize - np.count_nonzero(matrix))
    return score

@njit(fastmath=True)
def getDistinct(matrix):
    return np.unique(matrix).size


@njit(fastmath=True)
def evaluate_neighbors(matrix):
    non_zero_horizontal_neighbors = np.sum((matrix[:, :-1] != 0) & (matrix[:, :-1] == matrix[:, 1:]))
    non_zero_vertical_neighbors = np.sum((matrix[:-1, :] != 0) & (matrix[:-1, :] == matrix[1:, :]))
    return non_zero_horizontal_neighbors + non_zero_vertical_neighbors


@njit(fastmath=True)
def evaluate_smoothness(matrix):
    non_zero_row_diff = np.abs(matrix[:, :-1][matrix[:, :-1] != 0] - matrix[:, 1:][matrix[:, 1:] != 0])
    non_zero_column_diff = np.abs(matrix[:-1, :][matrix[:-1, :] != 0] - matrix[1:, :][matrix[1:, :] != 0])
    smoothness = np.sum(non_zero_row_diff) + np.sum(non_zero_column_diff)
    return smoothness


@njit(fastmath=True)
def max_tile(matrix):
    return np.max(matrix)

@njit(fastmath=True)
def evaluate_empty_cells(matrix):
    all_cells = matrix.size
    empty_cells = all_cells - np.count_nonzero(matrix)
    return empty_cells