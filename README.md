# 2048-game-AI

## Variação do algoritmo Monte Carlo Tree Search jogando 2048

### Descrição do problema

2048 é um jogo de tabuleiro em que o jogador deve mover as peças para que elas se somem e formem o número 
2048 ou maior. O tabuleiro é uma matriz 4x4, e a cada jogada uma nova peça é adicionada ao tabuleiro, com valor 2 ou 4. O jogador pode mover as peças para cima, baixo, esquerda ou direita, e todas as peças se movem na mesma direção até que encontrem outra peça ou a borda do tabuleiro. Quando duas peças com o mesmo valor se encontram, elas se somam e formam uma peça com o dobro do valor. O jogo termina quando o jogador consegue formar uma peça com o valor 2048, ou quando não há mais movimentos possíveis.

### Descrição da solução

Na variação implementada do algoritmo MCTS buscamos por um "Melhor movimento", ou seja, queremos de alguma forma descobrir qual é o melhor movimento para a situação do tabuleiro atual. O método que utilizei foi buscar por centenas ou milhares de jogos totalmente aleatórios o 'Evaluation', nesse caso a pontuação do tabuleiro.

Simulamos X jogos divididos em 4 partes:
1. Jogos que o primeiro movimento é a esquerda
2. Jogos que o primeiro movimento é a direita
3. Jogos que o primeiro movimento é para cima
4. Jogos que o primeiro movimento é para baixo

Após simular X jogos tiramos a média da pontuação final de cada, sendo a maior média o possível melhor movimento.

Em cada simulação vemos Y (Depth) movimentos a frente, ou seja, se Y = 2, vemos o tabuleiro atual e os próximos 2 movimentos, e assim por diante.

### Resultados

Após simular 20 jogos 4x4, obtivemos os resultados:
- 2048: 100%
- 4096: 35%

### Como executar

Para executar o programa basta rodar o comando:
```
python3 Algorithm.py
```

### Otimizações

Para otimizar o algoritmo, utilizamos a biblioteca Numba, que compila o código Python para código de máquina, e assim, aumenta a velocidade de execução do programa.

Além de vários outros métodos de otimização, como tornar as váriaveis de iteração (depth e max_iter) dinâmicas com o 
decorrer do jogo.

### Dependências

- Python 3.6
- Numpy
- Numba

### Referências

- [2048](https://en.wikipedia.org/wiki/2048_(video_game))
- [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)
- [Numba](https://numba.pydata.org/)
- [2048 Game](https://2048.org/)

### Observações

- O método de pontuação utilizado não foi o mesmo do site 2048.org, por exemplo, nesse programa utilizei apenas as somas de todos os valores dos tiles.

### Autor
[João Victor](https://github.com/JoaoVictor-C)