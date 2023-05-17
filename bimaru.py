# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 69:
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
    def __init__(self, board, row_counts, column_counts, len_row, len_column):
        self.board = board
        self.row_counts = row_counts
        self.column_counts = column_counts
        self.LEN_ROW = len_row
        self.LEN_COLUMN = len_column

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN:
            if self.board[row][col] == '*':
                return None
            else:
                return str(self.board[row][col])
        return None

    def get_row_counts(self):
        return self.row_counts

    def get_column_counts(self):
        return self.column_counts

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return self.get_value(row - 1, col), self.get_value(row + 1, col)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return self.get_value(row, col - 1), self.get_value(row, col + 1)

    def set_value(self, row, col, val):
        """Devolve um board com um novo elemento, na posição introdu
        zida"""
        if 0 <= row <= 9 and 0 <= col <= 9:
            self.board[row][col] = val
            if val != '.':
                self.row_counts[row] -= 1
                self.column_counts[col] -= 1
        # eh mesmo necessario retornar a board?
        return self.board

    def print(self):
        np.savetxt(sys.stdout, self.board, delimiter=' ', fmt='%s')
        print("\n")

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        LEN_ROW = 10
        LEN_COLUMN = 10
        row_counts = [int(val) for val in sys.stdin.readline().split()[1:]]
        column_counts = [int(val) for val in sys.stdin.readline().split()[1:]]
        numOfHints = int(sys.stdin.readline())
        hints = []
        board = np.full((LEN_ROW, LEN_COLUMN), "*")

        for i in range(numOfHints):
            hint = sys.stdin.readline().split()[1:]
            hints.append(tuple(hint))

        for hint in hints:
            row_idx, col_idx, letter = hint
            board[int(row_idx)][int(col_idx)] = letter

        return Board(board, row_counts, column_counts, LEN_ROW, LEN_COLUMN)

    def fill_section_with_water(self):
        """Recebe um board, nas linhas e/ou colunas onde o número de
        barcos restantes for zero, a função preenche com água"""

        for i in range(self.LEN_ROW):
            if self.row_counts[i] == 0:
                for j in range(self.LEN_COLUMN):
                    if self.get_value(i, j) is None:
                        self.set_value(i, j, '.')

        for i in range(self.LEN_COLUMN):
            if self.column_counts[i] == 0:
                for j in range(self.LEN_ROW):
                    if self.get_value(j, i) is None:
                        self.set_value(j, i, '.')
        return self.board

    def circle_single_boat_with_water(self, row, col):
        self.set_value(row - 1, col, ".")
        self.set_value(row + 1, col, ".")
        self.set_value(row, col - 1, ".")
        self.set_value(row, col + 1, ".")
        self.set_value(row - 1, col - 1, ".")
        self.set_value(row - 1, col + 1, ".")
        self.set_value(row + 1, col - 1, ".")
        self.set_value(row + 1, col + 1, ".")

    def is_board_fully_filled(self) -> bool:
        for i in self.get_row_counts():
            if i != 0:
                return False
        for i in self.get_column_counts():
            if i != 0:
                return False
        return True

    def count_boats(self) -> tuple:
        board_copy = self
        num_submarines = 0
        num_cruisers = 0
        num_destroyers = 0
        num_battleships = 0

        for i in range(self.LEN_ROW):
            for j in range(self.LEN_COLUMN):
                if board_copy.get_value(i, j) == 'C':
                    num_submarines += 1
                elif board_copy.get_value(i, j) == 'T':
                    if board_copy.get_value(i + 1, j) == 'B':
                        num_cruisers += 1
                        board_copy.set_value(i + 1, j, 'X')






class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)
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

        state.board.set_value(action[0], action[1], action[2])
        return BimaruState(state.board)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler grelha do ficheiro 'i1.txt' (Figura 1):
    # $ python3 bimaru.py < i1.txt
    board = Board.parse_instance()
    board.circle_single_boat_with_water(9, 5)
    board.circle_single_boat_with_water(3, 2)
    board.print()
    board.fill_section_with_water()
    board.print()
    print(board.get_row_counts())
    print(board.get_column_counts())
    pass
