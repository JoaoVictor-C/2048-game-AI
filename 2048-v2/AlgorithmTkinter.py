import numpy as np
import tkinter as tk
import numba as nb

from Evaluate import *
from Game import *

backgroundColor = {
    1: '#eee4da',
    2: '#ede0c8',
    3: '#f2b179',
    4: '#f59563',
    5: '#f59563',
    6: '#f65e3b',
    7: '#edcf72',
    8: '#edcc61',
    9: '#edc850',
    10: '#edc53f',
    11: '#edc22e',
    12: '#b8850a',
    13: '#af7505',

}
tileColor = {
    1: '#776e65',
    2: '#776e65',
    3: '#f9f6f2',
    4: '#f9f6f2',
    5: '#f9f6f2',
    6: '#f9f6f2',
    7: '#f9f6f2',
    8: '#f9f6f2',
    9: '#f9f6f2',
    10: '#f9f6f2',
    11: '#f9f6f2',
    12: '#f9f6f2',
    13: '#f9f6f2',
}

backgroundC = '#bbada0'

gridSize = 5

class Game2048(tk.Frame):
    def __init__(self, master=tk.Tk()):
        super().__init__(master)
        self.matrix = None
        self.master = master
        self.master.title('2048')
        self.master.rowconfigure(1)
        self.master.columnconfigure(1)
        self.gameArea = tk.Frame(self.master, bg=backgroundC, padx=7, pady=7)
        self.gameArea.grid(row=1, column=1)
        self.master.bind('<Escape>', lambda e: self.master.destroy())
        self.master.update_idletasks()
        self.master.update()
        self.master.bind('<Key>', self.move)
        self.score = 0
        self.init_game()

    def init_game(self):
        self.score = 0
        self.matrix = np.zeros((gridSize, gridSize), dtype=np.int32)
        self.matrix = add_random_num(self.matrix)
        self.matrix = add_random_num(self.matrix)
        self.draw_matrix(self.matrix)
        self.draw_score()
        self.master.update()

    def move(self, event):
        moves = {0: move_up, 1: move_down, 2: move_left, 3: move_right,
                 'Up': move_up, 'Down': move_down, 'Left': move_left, 'Right': move_right}
        if event in moves:
            self.matrix = moves[event](self.matrix)
        elif event.keysym in moves:
            self.matrix = moves[event.keysym](self.matrix)
        self.score = evaluate(self.matrix)
        self.draw_matrix(self.matrix)
        self.draw_score()
        self.master.update()

    def draw_matrix(self, matrix):
        for widget in self.gameArea.winfo_children():
            widget.destroy()
        for i in range(gridSize):
            for j in range(gridSize):
                responsiveTextSize = 160 // gridSize
                tile = tk.Label(self.gameArea, text=str(np.power(2, matrix[i][j])) if matrix[i][j] != 0 else '',
                                font=('Clear Sans', responsiveTextSize, 'bold'),
                                width=4, height=2, bg=backgroundColor[matrix[i][j]] if matrix[i][j] != 0 else '#cdc1b4',
                                fg=tileColor[matrix[i][j]] if matrix[i][j] != 0 else '#776e65')
                tile.grid(row=i, column=j, padx=7, pady=7)

    def draw_score(self):
        tk.Label(self.master, text='Score: ' + str(self.score), font=('Clear Sans', 25, 'bold')).grid(row=0, column=1)

    def draw_status(self, iterations, best_move, total_moves, depth):
        for widget in self.master.winfo_children():
            if widget != self.gameArea and widget != self.master.winfo_children()[1] and widget != self.master.winfo_children()[2]:
                widget.destroy()
        move = {0: 'Cima', 1: 'Baixo', 2: 'Esquerda', 3: 'Direita'}
        move = move[best_move]
        tk.Label(self.master, text='Simulações: ' + str(iterations), font=('Clear Sans', 25, 'bold')).grid(row=0, column=0)
        tk.Label(self.master, text='Último movimento: ' + str(move), font=('Clear Sans', 25, 'bold'), width=23).grid(row=2, column=0)
        tk.Label(self.master, text='Movimentos: ' + str(total_moves), font=('Clear Sans', 25, 'bold')).grid(row=2, column=2)
        tk.Label(self.master, text='Profundidade: ' + str(depth), font=('Clear Sans', 25, 'bold')).grid(row=0, column=2)

@nb.jit(fastmath=True, parallel=True)
def random_move(matrix, temp_move, first_move):
    moves = [move_up, move_down, move_left, move_right]
    if temp_move is None:
        temp_move = moves[first_move]
    else:
        temp_move = moves[np.random.randint(0, 4)]
    matrix = temp_move(matrix)
    return matrix, first_move, temp_move

@nb.jit(fastmath=True, parallel=True)
def random_game(matrix, first_move, depth=150):
    temp_move=None
    for i in range(depth):
        matrix, first_move, temp_move = random_move(matrix.copy(), temp_move, first_move)
        if is_game_over(matrix):
            break
    score = evaluate(matrix)
    return score, first_move



class MCTS:
    def __init__(self, game, max_iter=2000):
        self.game = game
        self.max_iter = max_iter
        self.totalMoves = 0

    def get_move(self, matrix, iterations):
        iteration = iterations // 4
        moves_iterations = {0: iteration, 1: iteration, 2: iteration, 3: iteration}
        depth = 40
        emptyCells = evaluate_empty_cells(self.game.matrix)
        if emptyCells <= gridSize * gridSize * 0.08:
            depth *= 2.5
        elif emptyCells <= gridSize * gridSize * 0.225:
            depth *= 2
        elif emptyCells <= gridSize * gridSize * 0.35:
            depth *= 1.5
        elif emptyCells <= gridSize * gridSize * 0.5:
            depth *= 1
        elif emptyCells <= gridSize * gridSize * 0.75:
            depth *= 0.75
        else:
            depth *= 0.5

        neighbors = evaluate_neighbors(self.game.matrix)
        if neighbors == 0:
            depth *= 2
        elif neighbors <= 4:
            depth *= 0.75
        else:
            depth *= 0.5

        depth = int(depth)
        allMoves = np.array([{}])
        for move, iteration in moves_iterations.items():
            for i in range(iteration):
                score, first_move = random_game(matrix.copy(), move, depth)
                if allMoves[0].get(move) is None:
                    allMoves[0][move] = score
                else:
                    allMoves[0][move] += score


        bestMove = -1
        bestScore = -1

        for move in range(4):
            score = 0
            for i in range(len(allMoves)):
                if move in allMoves[i]:
                    score += allMoves[i][move]
            score /= len(allMoves)
            if score > bestScore:
                bestScore = score
                bestMove = move
        self.game.draw_status(iterations, bestMove, self.totalMoves, depth)
        return bestMove

    def play(self):
        running = True
        while running:
            matrix = self.game.matrix.copy()
            iterations = self.get_best_maxIterations()
            move = self.get_move(matrix, iterations)
            self.game.move(move)
            self.totalMoves += 1
            if is_game_over(self.game.matrix):
                running = False
                break

        print('Game Over')
        print('Score: ', self.game.score)

    def get_best_maxIterations(self):
        iterations = 0
        emptyCells = evaluate_empty_cells(self.game.matrix)

        if emptyCells <= gridSize * gridSize * 0.08:
            iterations += self.max_iter // 5
        elif emptyCells <= gridSize * gridSize * 0.225:
            iterations += self.max_iter // 10
        elif emptyCells <= gridSize * gridSize * 0.35:
            iterations += self.max_iter // 20
        elif emptyCells <= gridSize * gridSize * 0.5:
            iterations += self.max_iter // 30
        elif emptyCells <= gridSize * gridSize * 0.75:
            iterations += self.max_iter // 40
        else:
            iterations += self.max_iter // 50

        neighbors = evaluate_neighbors(self.game.matrix)
        if neighbors == 0:
            iterations *= 2
        elif neighbors <= 2:
            iterations *= 1
        elif neighbors <= 4:
            iterations *= 0.75
        else:
            iterations *= 0.5
        iterations += self.totalMoves * ((gridSize * gridSize) / 16 * 0.05)
        iterations = int(iterations)

        return iterations


if __name__ == '__main__':
    game = Game2048()
    mcts = MCTS(game)
    mcts.play()
    while True:
        game.master.update_idletasks()
        game.master.update()