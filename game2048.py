import tkinter as tk
import numpy as np
import kivy as kv
import timeit


backgroundColor = {
    2: '#eee4da',
    4: '#ede0c8',
    8: '#f2b179',
    16: '#f59563',
    32: '#f59563',
    64: '#f65e3b',
    128: '#edcf72',
    256: '#edcc61',
    512: '#edc850',
    1024: '#edc53f',
    2048: '#edc22e',
    4096: '#b8850a',
    8192: '#af7505',

}

tileColor = {
    2: '#776e65',
    4: '#776e65',
    8: '#f9f6f2',
    16: '#f9f6f2',
    32: '#f9f6f2',
    64: '#f9f6f2',
    128: '#f9f6f2',
    256: '#f9f6f2',
    512: '#f9f6f2',
    1024: '#f9f6f2',
    2048: '#f9f6f2',
    4096: '#f9f6f2',
    8192: '#f9f6f2',
}

background = '#bbada0'

def add_random_num(matrix):
    zero_list = []
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                zero_list.append((i, j))
    if len(zero_list) == 0:
        return matrix
    index = np.random.randint(0, len(zero_list))
    i, j = zero_list[index]
    matrix[i][j] = 2 if np.random.random() < 0.9 else 4
    return matrix

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
                    matrix[i][j] *= 2
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
    return matrix

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
                    matrix[i][j] *= 2
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
    return matrix

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
                    matrix[i][j] *= 2
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
    return matrix

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
                    matrix[i][j] *= 2
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
    return matrix

def get_score(matrix):
    score = 0
    for i in range(4):
        for j in range(4):
            score += matrix[i][j]
    return score

def is_game_over(matrix):
    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 0:
                return False
    for i in range(4):
        for j in range(3):
            if matrix[i][j] == matrix[i][j + 1]:
                return False
    for j in range(4):
        for i in range(3):
            if matrix[i][j] == matrix[i + 1][j]:
                return False
    return True

class Game2048(tk.Frame):
    def __init__(self, master=tk.Tk()):
        super().__init__(master)
        self.matrix = None
        self.master = master
        self.master.title('2048')
        self.master.geometry('500x500')
        self.master.resizable(0, 0)
        self.master.bind('<Key>', self.move)
        self.score = 0
        self.pack()
        self.init_game()

    def init_game(self):
        self.score = 0
        self.matrix = np.zeros((4, 4), dtype=np.int32)
        self.matrix = add_random_num(self.matrix)
        self.matrix = add_random_num(self.matrix)
        self.draw_matrix(self.matrix)
        self.draw_score()
        self.master.update()

    def move(self, event):
        moves = {0: move_up, 1: move_down, 2: move_left, 3: move_right,
                 'Up': move_up, 'Down': move_down, 'Left': move_left, 'Right': move_right}
        if event in moves:
            moves[event](self.matrix)
        self.score = get_score(self.matrix)
        self.matrix = add_random_num(self.matrix)
        self.draw_matrix(self.matrix)
        self.draw_score()
        if is_game_over(self.matrix):
            self.init_game()
        self.master.update()

    def draw_matrix(self, matrix):
        for widget in self.winfo_children():
            widget.destroy()
        for i in range(4):
            for j in range(4):
                tk.Label(self, text=str(matrix[i][j]) if matrix[i][j] != 0 else '', font=('Arial', 20), width=4, height=2,
                         bg=backgroundColor[matrix[i][j]] if matrix[i][j] != 0 else '#cdc1b4',
                         fg=tileColor[matrix[i][j]] if matrix[i][j] != 0 else '#f9f6f2').grid(row=i, column=j, padx=5, pady=5)

    def draw_score(self):
        tk.Label(self, text='Score: ' + str(self.score), font=('Arial', 20)).grid(row=4, column=0, columnspan=4)



# Iremos refazer a classe Game2048 porém agora usando a biblioteca Kivy


class RandomGame2048:
    def __init__(self, matrix):
        self.temp_move = None
        self.matrix = matrix
        self.score = 0
        self.first_move = None

    def random_move(self, index_move=None):
        moves = [move_up, move_down, move_left, move_right]
        if self.temp_move is None:
            if index_move is not None:
                self.temp_move = moves[index_move]
                self.first_move = index_move
            else:
                self.temp_move = np.random.choice(moves)
                self.first_move = moves.index(self.temp_move)
        else:
            self.temp_move = np.random.choice(moves)
        self.matrix = self.temp_move(self.matrix)
        add_random_num(self.matrix)
        return self.matrix

    def random_game(self, index_move=None):
        while not is_game_over(self.matrix):
            self.matrix = self.random_move(index_move)
            self.score = get_score(self.matrix)
        return self.score, self.first_move


class MCTS:
    def __init__(self, game, max_iter=1000, temperature=0.75):
        self.game = game
        self.max_iter = max_iter
        self.totalMoves = 0
        self.original_max_iter = max_iter
        self.temperature = temperature
        self.LastIterations = 0

    def get_move(self, matrix, iterations):
        iteration = iterations // 4
        moves_iterations = {0: iteration, 1: iteration, 2: iteration, 3: iteration}

        allMoves = []

        for move, iteration in moves_iterations.items():
            for i in range(iteration):
                game = RandomGame2048(matrix.copy())
                score, first_move = game.random_game(move)
                allMoves.append({first_move: score})
        bestMove = -1
        bestScore = -1
        # agrupa os scores de cada movimento e tira a média
        for move in range(4):
            score = 0
            for i in range(len(allMoves)):
                if list(allMoves[i].keys())[0] == move:
                    score += list(allMoves[i].values())[0]
            score /= moves_iterations[move]
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestMove

    def play(self):
        running = True
        while running:
            matrix = self.game.matrix.copy()
            iterations = self.get_best_maxIterations()
            move = self.get_move(matrix, iterations)
            self.game.move(move)
            self.totalMoves += 1
            # Se não existir o txt com o melhor total de movimentos, cria um

            with open('bestTotalMoves.txt', 'r') as f:
                if f.read() == '':
                    with open('bestTotalMoves.txt', 'w') as f:
                        f.write(str(self.totalMoves))
                bestTotalMoves = int(f.read())
            if self.totalMoves > bestTotalMoves:
                with open('bestTotalMoves.txt', 'w') as f:
                    f.write(str(self.totalMoves))

            if is_game_over(self.game.matrix):
                running = False

        print('Game Over')
        print('Score: ', self.game.score)

    def get_best_maxIterations(self):
        iterations = 0
        with open('bestTotalMoves.txt', 'r') as f:
            bestTotalMoves = int(f.read())
        if self.totalMoves <= 0.01 * bestTotalMoves:
            iterations = self.max_iter // 100
        elif self.totalMoves <= 0.1 * bestTotalMoves:
            iterations = self.max_iter // 50
        elif self.totalMoves <= 0.25 * bestTotalMoves:
            iterations = self.max_iter // 25
        elif self.totalMoves <= 0.5 * bestTotalMoves:
            iterations = self.max_iter // 10
        elif self.totalMoves <= 0.75 * bestTotalMoves:
            iterations = self.max_iter // 5
        elif self.totalMoves <= 0.9 * bestTotalMoves:
            iterations = self.max_iter // 2
        else:
            iterations = self.max_iter
        print('Total Moves: ', self.totalMoves)
        print('Iterations: ', iterations)
        if self.totalMoves % 10 == 0:
            if self.LastIterations == 0:
                timer = timeit.Timer(lambda: self.get_move(self.game.matrix.copy(), iterations))
            else:
                timer = timeit.Timer(lambda: self.get_move(self.game.matrix.copy(), self.LastIterations))
            print('Time: ', timer.timeit(1))
            if timer.timeit(1) > self.temperature:
                self.max_iter = self.max_iter // 2
                print('Max Iterations: ', self.max_iter)
            else:
                self.max_iter = self.original_max_iter
                print('Max Iterations: ', self.max_iter)
        self.LastIterations = iterations
        return iterations


if __name__ == '__main__':
    game = Game2048()
    mcts = MCTS(game)
    mcts.play()
