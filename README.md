# 2048 Game AI

This project implements a variation of the Monte Carlo Tree Search algorithm to play the game 2048.

## Problem Description

2048 is a board game where the player must combine tiles to form the number 2048 or higher. The board is a 4x4 matrix, and with each move, a new tile with a value of 2 or 4 is added. The player can move tiles in four directions: up, down, left, or right. Tiles move in the chosen direction until they encounter another tile or the edge of the board. When two tiles with the same value collide, they merge into one tile with double the value. The game ends when the player creates a tile with the value 2048 or when there are no more possible moves.

## Solution Description

In this variation of the Monte Carlo Tree Search algorithm, the goal is to find the best move for the current board situation. The approach involves simulating hundreds or thousands of random games to evaluate the board score. The implementation considers four sets of games based on the first move direction: left, right, up, and down. After simulating the games, the average final score is calculated for each set, and the move with the highest average score is considered the best move. The simulation also looks ahead a specified number of moves (depth) to evaluate potential future states.

## Results

After simulating 100 games of 4x4, the following results were obtained:

- 2048: 100%
- 4096: 34%
- 8.192: 1%

## How to Run

To execute the program, run the following command:

python3 Algorithm.py

markdown
Copy code

## Optimizations

To optimize the algorithm, the project utilizes the Numba library, which compiles Python code into machine code for faster execution. Additionally, several other optimization techniques are employed, such as dynamically adjusting iteration variables based on game progress.

## Dependencies

- Python 3.6
- Numpy
- Numba

## References

- [2048](https://en.wikipedia.org/wiki/2048_(video_game))
- [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
- [Numba](http://numba.pydata.org/)

## Notes

The scoring method used in this implementation differs from that of the website 2048.org. Only the sum of all tile values is considered in this program.

## Author

João Victor
