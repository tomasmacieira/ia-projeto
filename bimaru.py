# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board, pos_filled_row, pos_filled_column):
        self.board = board
        self.pos_filled_row = pos_filled_row
        self.filled_pos_column = pos_filled_column
        self.LEN_ROW = 10
        self.LEN_COLUMN = 10

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row <= self.LEN_ROW and  0 <= col <= self.LEN_COLUMN:
            return str(self.board[row][col])
        else:
            raise ValueError #??? dont know what to raise here

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            return (None, self.get_value(row + 1, col))
        elif row == 9:
            return (self.get_value(row + 1, col), None)
        return (self.get_value(row - 1,col),self.get_value(row + 1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            return (None, self.get_value(row, col + 1))
        elif col == 9:
            return (self.get_value(row, col - 1), None) 
        return (self.get_value(row, col - 1), self.get_value(row, col + 1))

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        filled_pos_row = list(sys.stdin.readline().split()[1:])
        filled_pos_column = list(sys.stdin.readline().split()[1:])
        numOfHints = int(sys.stdin.readline())
        hints = []

        for i in range(numOfHints):
            hint = sys.stdin.readline().split()[1:]
            hints.append(tuple(hint))

        board = np.full((10, 10), ".")

        for hint in hints:
            row_idx, col_idx, letter = hint
            board[int(row_idx)][int(col_idx)] = letter

        return Board(board, filled_pos_row, filled_pos_column)

    def print(self):
        np.savetxt(sys.stdout, self.board, delimiter=' ', fmt='%s')

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe

board = Board.parse_instance()
board.print()
print("\n")
print(board.get_value(1,6))
print("\n")
print(board.adjacent_horizontal_values(5,9))
print(board.adjacent_vertical_values(0,5))



if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
