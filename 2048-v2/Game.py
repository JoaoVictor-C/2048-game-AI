from numba import njit
import numpy as np

gridSize = 4

@njit(fastmath=True)
def add_random_num(matrix):
    zero_indices = np.argwhere(matrix == 0)
    if len(zero_indices) == 0:
        return matrix

    index = np.random.randint(0, len(zero_indices))
    i, j = zero_indices[index]

    matrix[i, j] = 1 if np.random.random() < 0.9 else 2

    return matrix


# Essa função pode receber uma matriz e um booleano que indica se a linha ou coluna deve ser revertida.
@njit(fastmath=True)
def merge_and_shift(matrix, reverse):
    new_matrix = np.zeros_like(matrix)

    # Para cada linha da matriz
    for i in range(gridSize):
        if not reverse:
            line = matrix[i, :]  # Pega a linha
        else:
            line = matrix[i, ::-1]  # Inverte a linha

        j = 0
        k = 0
        # Para cada elemento da linha
        while j < gridSize:
            if line[j] != 0:
                if j < (gridSize - 1) and line[j] == line[j + 1]:  # Se o elemento atual for igual ao próximo
                    new_value = line[j] + 1
                    j += 1
                else:
                    new_value = line[j]
                new_matrix[i, k] = new_value
                k += 1
            j += 1

    if reverse:  # Se a linha ou coluna foi revertida, inverte novamente
        new_matrix = new_matrix[:, ::-1]

    return add_random_num(new_matrix)

'''
O método transpose() gira o tabuleiro em 90 graus
A função merge_and_shift() pode ser usada para mover para as 4 direções
Ao colocar o parâmetro reverse=True, a função move_and_shift() irá inverter a linha ou coluna
'''

@njit(fastmath=True)
def move_up(matrix):
    return merge_and_shift(matrix.transpose(), False).transpose()

@njit(fastmath=True)
def move_down(matrix):
    return merge_and_shift(matrix.transpose(), True).transpose()

@njit(fastmath=True)
def move_left(matrix):
    return merge_and_shift(matrix, False)

@njit(fastmath=True)
def move_right(matrix):
    return merge_and_shift(matrix, True)

@njit(fastmath=True)
def is_game_over(matrix):
    gridSize = matrix.shape[0]
    for i in range(gridSize):
        for j in range(gridSize):
            if matrix[i, j] == 0:
                return False

    for i in range(gridSize):
        for j in range(gridSize - 1):
            if matrix[i, j] == matrix[i, j + 1]:
                return False
            if matrix[j, i] == matrix[j + 1, i]:
                return False

    return True
