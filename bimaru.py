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

    def __init__(self, board, row_counts, column_counts, hints, len_row, len_column, num_boats_to_add, isCopy):
        self.board = board
        self.row_counts = row_counts
        self.column_counts = column_counts
        self.hints = hints
        self.LEN_ROW = len_row
        self.LEN_COLUMN = len_column
        if isCopy:
            self.num_boats_to_add = num_boats_to_add
        else:
            self.num_boats_to_add = self.count_boats_to_add()
            self.process_board()

    def process_board(self):
        for hint in self.hints:
            row, col, value = hint
            row = int(row)
            col = int(col)
            if value == 'C':
                self.circle_single_boat_with_water(row, col)
            elif value == 'T':
                self.circle_top_of_boat_with_water(row, col)
            elif value == 'B':
                self.circle_bottom_of_boat_with_water(row, col)
            elif value == 'M':
                self.circle_middle_of_boat_with_water(row, col)
            elif value == 'L':
                self.circle_left_of_boat_with_water(row, col)
            elif value == 'R':
                self.circle_right_of_boat_with_water(row, col)
        self.fill_sections_with_water()

    def count_boats_to_add(self) -> list:
        num_submarines = 4
        num_cruisers = 3
        num_destroyers = 2
        num_battleships = 1

        for i in range(self.LEN_COLUMN):
            for j in range(self.LEN_ROW):
                value = self.get_value(j, i)
                if value == 'c':
                    num_submarines -= 1
                elif value == 't':
                    if self.get_value(j + 1, i) == 'b':
                        num_cruisers -= 1
                        j -= 1
                    elif self.get_value(j + 1, i) == 'm':
                        if self.get_value(j + 2, i) == 'm' \
                                and self.get_value(j + 3, i) == 'b':
                            num_battleships -= 1
                            j += 3
                        elif self.get_value(j + 2, i) == 'b':
                            num_destroyers -= 1
                            j += 2
                elif value == 'l':
                    if self.get_value(j, i + 1) == 'r':
                        num_cruisers -= 1
                    elif self.get_value(j, i + 1) == 'm':
                        if self.get_value(j, i + 2) == 'm' \
                                and self.get_value(j, i + 3) == 'r':
                            num_battleships -= 1
                        elif self.get_value(j, i + 2) == 'r':
                            num_destroyers -= 1

        return [num_submarines, num_cruisers, num_destroyers, num_battleships]

    @classmethod
    def from_board(cls, board):
        """ este metodo foi criada para testar a funcao count_boats e serve para se conseguir ler um
        input que contem uma board ja feita (como os .out do projeto). Deve possivelmente ser removido quando
        o projeto for concluido. """
        return cls(board, None, None, None, 10, 10, [], True)

    def copy(self):
        """Creates a copy of the Board."""
        new_board = np.copy(self.board)
        new_row_counts = self.row_counts.copy()
        new_column_counts = self.column_counts.copy()
        new_hints = self.hints.copy()
        new_num_boats_to_add = self.num_boats_to_add
        return Board(new_board, new_row_counts, new_column_counts, new_hints, self.LEN_ROW, self.LEN_COLUMN,
                     new_num_boats_to_add, True)

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN:
            if self.board[row][col] == '*':
                return "None"
            else:
                return str(self.board[row][col]).lower()
        return "None"

    def set_value(self, row, col, val):
        """Devolve um board com um novo elemento, na posição introduzida"""
        if 0 <= row <= 9 and 0 <= col <= 9 and self.board[row][col] != 'W':
            self.board[row][col] = val
            if val != 'w':
                self.row_counts[row] -= 1
                self.column_counts[col] -= 1
                if self.row_counts[row] == 0:
                    self.fill_row_with_water(row)
                if self.column_counts[col] == 0:
                    self.fill_column_with_water(col)

    def fill_row_with_water(self, row):
        for col in range(self.LEN_COLUMN):
            if self.get_value(row, col) == "None":
                self.set_value(row, col, 'w')

    def fill_column_with_water(self, col):
        for row in range(self.LEN_ROW):
            if self.get_value(row, col) == "None":
                self.set_value(row, col, 'w')

    def fill_sections_with_water(self):
        """Recebe um board, nas linhas e/ou colunas onde o número de
        barcos restantes for zero, a função preenche com água"""
        for row in range(self.LEN_ROW):
            if self.row_counts[row] == 0:
                self.fill_row_with_water(row)

        for col in range(self.LEN_COLUMN):
            if self.column_counts[col] == 0:
                self.fill_column_with_water(col)

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
            if letter != 'W':
                row_counts[int(row_idx)] -= 1
                column_counts[int(col_idx)] -= 1
            board[int(row_idx)][int(col_idx)] = letter

        return Board(board, row_counts, column_counts, hints, LEN_ROW, LEN_COLUMN, [], False)

    # Important still doing it. Have to do what kind of ships can be added in each position
    def possible_actions(self):
        """Devolve uma lista com possiveis acoes i.e: posicoes livres
        onde eh possivel introduzir um barco"""
        possible_actions = []

        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):
                if self.get_value(row, col) == "None":
                    possible_actions.append((row, col, "t"))
                    possible_actions.append((row, col, "b"))
                    possible_actions.append((row, col, "c"))
                    possible_actions.append((row, col, "m"))
        return possible_actions

    """
    def fill_obvious_spaces(self):
        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):
                available_positions = []
                empty_spaces = 0
                if self.board[row][col] == '*':
                    empty_spaces +=
                    available_positions.append(tuple(row,col))
            if empty_spaces == self.row_counts:
                for i in available_positions:
    """

    def is_board_fully_filled(self) -> bool:
        for i in self.row_counts:
            if i != 0:
                return False
        for i in self.column_counts:
            if i != 0:
                return False
        return True

    def add_value_and_circle_with_water(self, action):
        row, col, value = action
        self.set_value(row, col, value)

        if value == 'c':
            self.circle_single_boat_with_water(row, col)
            self.reduce_num_of_boats_to_add_with_size_n(1)
        elif value == 't':
            self.circle_top_of_boat_with_water(row, col)
            if self.get_value(row + 1, col) == 'b':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_value(row + 1, col) == 'm':
                if self.get_value(row + 2, col) == 'b':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_value(row + 2, col) == 'm' and self.get_value(row + 3, col) == 'b':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif value == 'm':
            if self.get_value(row - 1, col) == 't' and self.get_value(row + 1, col) == 'b':
                self.reduce_num_of_boats_to_add_with_size_n(3)
            elif (self.get_value(row - 1, col) == 'm' and self.get_value(row - 2, col) == 't' and
                  self.get_value(row + 1, col) == 'b') or \
                    (self.get_value(row + 1, col) == 'm' and self.get_value(row - 1, col) == 't' and
                     self.get_value(row + 2, col) == 'b'):
                self.reduce_num_of_boats_to_add_with_size_n(4)
            elif self.get_value(row, col - 1) == 'l' and self.get_value(row, col + 1) == 'r':
                self.reduce_num_of_boats_to_add_with_size_n(3)
            elif (self.get_value(row, col - 1) == 'm' and self.get_value(row, col - 2) == 'l' and
                  self.get_value(row, col + 1) == 'r') or \
                    (self.get_value(row, col + 1) == 'm' and self.get_value(row, col - 1) == 'l' and
                     self.get_value(row, col + 1) == 'r'):
                self.reduce_num_of_boats_to_add_with_size_n(4)
        elif value == 'b':
            self.circle_bottom_of_boat_with_water(row, col)
            if self.get_value(row - 1, col) == 't':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_value(row - 1, col) == 'm':
                if self.get_value(row - 2, col) == 't':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_value(row - 2, col) == 'm' and self.get_value(row - 3, col) == 't':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif value == 'l':
            self.circle_left_of_boat_with_water(row, col)
            if self.get_value(row, col + 1) == 'r':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_value(row, col + 1) == 'm':
                if self.get_value(row, col + 2) == 'r':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_value(row, col + 2) == 'm' and self.get_value(row, col + 3) == 'r':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif value == 'r':
            self.circle_right_of_boat_with_water(row, col)
            if self.get_value(row, col - 1) == 'l':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_value(row, col - 1) == 'm':
                if self.get_value(row, col - 2) == 'l':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_value(row, col - 2) == 'm' and self.get_value(row, col - 3) == 'l':
                    self.reduce_num_of_boats_to_add_with_size_n(4)

    def circle_single_boat_with_water(self, row, col):
        self.set_value(row - 1, col, "w")
        self.set_value(row + 1, col, "w")
        self.set_value(row, col - 1, "w")
        self.set_value(row, col + 1, "w")
        self.set_value(row - 1, col - 1, "w")
        self.set_value(row - 1, col + 1, "w")
        self.set_value(row + 1, col - 1, "w")
        self.set_value(row + 1, col + 1, "w")

    def circle_top_of_boat_with_water(self, row, col):
        self.set_value(row - 1, col, "w")
        self.set_value(row - 1, col - 1, "w")
        self.set_value(row - 1, col + 1, "w")
        self.set_value(row, col - 1, "w")
        self.set_value(row, col + 1, "w")
        self.set_value(row + 1, col + 1, "w")
        self.set_value(row + 1, col - 1, "w")

    def circle_middle_of_boat_with_water(self, row, col):
        self.set_value(row - 1, col - 1, "w")
        self.set_value(row - 1, col + 1, "w")
        self.set_value(row + 1, col - 1, "w")
        self.set_value(row + 1, col + 1, "w")

    def circle_bottom_of_boat_with_water(self, row, col):
        self.set_value(row + 1, col, "w")
        self.set_value(row + 1, col - 1, "w")
        self.set_value(row + 1, col + 1, "w")
        self.set_value(row, col - 1, "w")
        self.set_value(row, col + 1, "w")
        self.set_value(row - 1, col - 1, "w")
        self.set_value(row - 1, col + 1, "w")

    def circle_left_of_boat_with_water(self, row, col):
        self.set_value(row - 1, col - 1, "w")
        self.set_value(row - 1, col, "w")
        self.set_value(row - 1, col + 1, "w")
        self.set_value(row, col - 1, "w")
        self.set_value(row + 1, col - 1, "w")
        self.set_value(row + 1, col, "w")
        self.set_value(row + 1, col + 1, "w")

    def circle_right_of_boat_with_water(self, row, col):
        self.set_value(row - 1, col - 1, "w")
        self.set_value(row - 1, col, "w")
        self.set_value(row - 1, col + 1, "w")
        self.set_value(row, col + 1, "w")
        self.set_value(row + 1, col - 1, "w")
        self.set_value(row + 1, col, "w")
        self.set_value(row + 1, col + 1, "w")

    def reduce_num_of_boats_to_add_with_size_n(self, n: int):
        self.num_boats_to_add[n - 1] -= 1

    # Para ser usado no "possible positions"
    def is_there_any_boats_with_size_n_to_add(self, n: int):
        return self.num_boats_to_add[n - 1] > 0

    def print(self):
        modified_board = np.where(self.board == 'w', '.', self.board)  # Replace 'w' with '.'
        np.savetxt(sys.stdout, modified_board, delimiter=' ', fmt='%s')
        print("\n")

    @staticmethod
    def get_board_output():
        """ este metodo foi criada para testar a funcao count_boats e serve para se conseguir ler um
           input que contem uma board ja feita (como os .out do projeto). Deve possivelmente ser removido quando
           o projeto for concluido. """
        board = np.empty((10, 10), dtype=str)
        for i in range(10):
            line = sys.stdin.readline().strip()
            for j in range(10):
                board[i][j] = line[j]
        return Board.from_board(board)


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return state.board.possible_actions()
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_board = state.board.copy()
        new_board.add_value_and_circle_with_water(action)
        return BimaruState(new_board)

    def goal_test(self, state: BimaruState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.is_board_fully_filled() and state.board.num_boats_to_add == [0, 0, 0, 0]
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

    # Exemplo 2
    """"
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    initial_state = BimaruState(board)
    # Mostrar valor na posição (3, 3):
    print(initial_state.board.get_value(3, 3))
    # Realizar acção de inserir o valor w (água) na posição da linha 3 e coluna 3
    result_state = problem.result(initial_state, (3, 3, 'w'))
    # Mostrar valor na posição (3, 3):
    print(result_state.board.get_value(3, 3))
    result_state.board.print_board() """

    # Exemplo 3
    # Criar uma instância de Bimaru:
    problem = Bimaru(board)
    # Criar um estado com a configuração inicial:
    s0 = BimaruState(board)
    print("Estado inicial da board:")
    s0.board.print()

    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (0, 6, 't'))
    s2 = problem.result(s1, (1, 0, 'b'))
    s3 = problem.result(s2, (1, 9, 't'))
    s4 = problem.result(s3, (2, 6, 'b'))
    s5 = problem.result(s4, (2, 9, 'm'))
    s6 = problem.result(s5, (3, 9, 'm'))
    s7 = problem.result(s6, (4, 0, 'c'))
    s8 = problem.result(s7, (4, 7, 'c'))
    s9 = problem.result(s8, (4, 9, 'b'))
    s10 = problem.result(s9, (6, 4, 't'))
    s11 = problem.result(s10, (7, 0, 't'))
    s12 = problem.result(s11, (7, 4, 'b'))
    s13 = problem.result(s12, (7, 8, 't'))
    s14 = problem.result(s13, (8, 0, 'm'))
    s15 = problem.result(s14, (9, 0, 'b'))
    # ...
    # não estão aqui apresentadas todas as ações
    # considere que s15 contém a solução final
    # Verificar se foi atingida a soluçãoz`
    print("Is goal?", problem.goal_test(s5))
    s5.board.print()
    print("Is goal?", problem.goal_test(s15))
    print("Solution:\n", s15.board.print(), sep="")

    """
    board.process_board()
    problem = Bimaru(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.print(), sep="")
    """
    pass
