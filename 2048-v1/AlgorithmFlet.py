import numba as nb
import flet as ft
from flet import TextField
import numpy as np

from Evaluate import evaluate, evaluate_empty_cells, evaluate_neighbors, evaluate_score
from Game import move_up, move_down, move_left, move_right, add_random_num, is_game_over

backgroundColor = {
    0: '#bbada0',
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
    0: '#776e65',
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
        score = evaluate(matrix)
        if is_game_over(matrix):
            break
    return score, first_move


class MCTS:
    def __init__(self, max_iter=1500):
        self.max_iter = max_iter
        self.totalMoves = 0
        self.original_max_iter = max_iter

    def get_move(self, matrix, iterations=1500):
        iteration = iterations // 4
        moves_iterations = {0: iteration, 1: iteration, 2: iteration, 3: iteration}
        depth = 30
        emptyCells = evaluate_empty_cells(matrix)
        if emptyCells <= 1:
            depth *= 3
        elif emptyCells <= 4:
            depth *= 2
        elif emptyCells <= 6:
            depth *= 1.5
        elif emptyCells <= 8:
            depth *= 1
        elif emptyCells <= 12:
            depth *= 0.75
        elif emptyCells <= 16:
            depth *= 0.5

        neighbors = evaluate_neighbors(matrix)
        if neighbors == 0:
            depth *= 2
        elif neighbors <= 2:
            depth *= 1
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
        return bestMove

    def play(self, matrix):
        iterations = self.get_best_maxIterations(matrix)
        move = self.get_move(matrix, iterations)
        match move:
            case 0:
                matrix = move_up(matrix)
            case 1:
                matrix = move_down(matrix)
            case 2:
                matrix = move_left(matrix)
            case 3:
                matrix = move_right(matrix)
        self.game.matrix = matrix.copy()
        self.totalMoves += 1
        return matrix


    def get_best_maxIterations(self, matrix):
        iterations = 0
        emptyCells = evaluate_empty_cells(matrix)
        if emptyCells <= 1:
            iterations += self.max_iter // 5
        elif emptyCells <= 4:
            iterations += self.max_iter // 10
        elif emptyCells <= 6:
            iterations += self.max_iter // 20
        elif emptyCells <= 8:
            iterations += self.max_iter // 30
        elif emptyCells <= 12:
            iterations += self.max_iter // 40
        elif emptyCells <= 16:
            iterations += self.max_iter // 50

        neighbors = evaluate_neighbors(matrix)
        if neighbors == 0:
            iterations *= 2
        elif neighbors <= 2:
            iterations *= 0.80
        elif neighbors <= 4:
            iterations *= 0.5
        else:
            iterations *= 0.25
        iterations += self.totalMoves // 10
        iterations = int(iterations)
        return iterations


def main(page, matrix=np.zeros((4, 4), dtype=np.int32)):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    page.window_title = "2048"
    matrix = matrix
    matrix = add_random_num(matrix)
    matrix = add_random_num(matrix)
    score = evaluate_score(matrix)
    cells = []
    scoreCell = ft.Text(value=f"Score: {score}", size=30)
    iaRunning = False
    Algorithm = MCTS(matrix)

    for row in matrix:
        for cell in row:
            cells.append(TextField(value=str(2 ** cell) if cell != 0 else "", width=100, height=100,
                                   text_size=30, bgcolor=backgroundColor[cell], color=tileColor[cell],
                                   text_align=ft.TextAlign.CENTER, disabled=True))

    def initState():
        page.add(
            ft.Row(
                [
                    ft.Text(value="2048", size=60, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    scoreCell,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.TextButton(
                        text="Restart",
                        on_click=lambda _: restart(),

                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    cells[0],
                                    cells[1],
                                    cells[2],
                                    cells[3],
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=13,
                            ),
                            ft.Row(
                                [
                                    cells[4],
                                    cells[5],
                                    cells[6],
                                    cells[7],
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=13,
                            ),
                            ft.Row(
                                [
                                    cells[8],
                                    cells[9],
                                    cells[10],
                                    cells[11],
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=13,
                            ),
                            ft.Row(
                                [
                                    cells[12],
                                    cells[13],
                                    cells[14],
                                    cells[15],
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=13,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def update():
        nonlocal cells
        nonlocal matrix
        nonlocal score

        for i, row in enumerate(matrix):
            for j, cell_value in enumerate(row):
                index = i * 4 + j
                cell = cells[index]
                cell.value = str(2 ** cell_value) if cell_value != 0 else ""
                cell.bgcolor = backgroundColor[cell_value]
                cell.color = tileColor[cell_value]

        for i in range(16):
            page.update(cells[i])
        scoreCell.value = f"Score: {score}"
        page.update(scoreCell)

    def initAIPlay():
        nonlocal Algorithm
        nonlocal iaRunning
        nonlocal score
        nonlocal matrix
        while iaRunning:
            move = Algorithm.get_move(matrix)
            match move:
                case 0:
                    matrix = move_up(matrix)
                case 1:
                    matrix = move_down(matrix)
                case 2:
                    matrix = move_left(matrix)
                case 3:
                    matrix = move_right(matrix)
            score = evaluate_score(matrix)
            update()




    def on_keyboard(e: ft.KeyboardEvent):
        nonlocal matrix
        nonlocal score
        if e.key == "Arrow Up":
            matrix = move_up(matrix)
        elif e.key == "Arrow Down":
            matrix = move_down(matrix)
        elif e.key == "Arrow Left":
            matrix = move_left(matrix)
        elif e.key == "Arrow Right":
            matrix = move_right(matrix)
        elif e.key == "Escape" or e.key == "R":
            restart()
            return
        elif e.key == "P":
            nonlocal iaRunning
            iaRunning = not iaRunning
            if iaRunning:
                initAIPlay()
            return
        score = evaluate_score(matrix)
        update()
    page.on_keyboard_event = on_keyboard

    def restart():
        nonlocal matrix
        nonlocal score
        page.clean()
        matrix = np.zeros((4, 4), dtype=np.int32)
        matrix = add_random_num(matrix)
        matrix = add_random_num(matrix)
        score = evaluate_score(matrix)
        update()

    def play():
        nonlocal matrix
        nonlocal score
        nonlocal iaRunning
        while iaRunning:
            matrix = Algorithm.play(matrix)
            score = evaluate_score(matrix)
            update()
            if is_game_over(matrix):
                iaRunning = False
                break

    initState()


if __name__ == '__main__':
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)