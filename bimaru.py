# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 69:
# 00000 Pedro Almeida
# 00000 Tomas Macieira

import sys
from search import (
    Problem,
    Node,
    depth_first_tree_search,
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


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board, num_vals_to_add_row, num_vals_to_add_col, og_num_vals_to_add_row, og_num_vals_to_add_col,
                 free_row_counts, free_col_counts, num_boats_to_add, unknown_vals_pos, added_boats, len_row, len_column,
                 isCopy):
        self.board = board
        self.num_vals_to_add_row = num_vals_to_add_row
        self.num_vals_to_add_col = num_vals_to_add_col
        self.og_num_vals_to_add_row = og_num_vals_to_add_row
        self.og_num_vals_to_add_col = og_num_vals_to_add_col
        self.free_row_counts = free_row_counts
        self.free_col_counts = free_col_counts
        self.unknown_vals_pos = unknown_vals_pos
        self.added_boats = added_boats
        self.LEN_ROW = len_row
        self.LEN_COLUMN = len_column
        if isCopy:
            self.num_boats_to_add = num_boats_to_add
        else:
            # self.num_boats_to_add = self.count_boats_to_add()
            self.process_board(True)
            self.num_boats_to_add = self.count_boats_to_add()

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
        num_vals_to_add_row = [int(num) for num in sys.stdin.readline().split()[1:]]
        num_vals_to_add_col = [int(num) for num in sys.stdin.readline().split()[1:]]
        og_num_vals_to_row = num_vals_to_add_row.copy()
        og_num_vals_to_col = num_vals_to_add_col.copy()
        free_row_counts = [10 for _ in range(10)]
        free_col_counts = [10 for _ in range(10)]
        numOfHints = int(sys.stdin.readline())
        hints = []
        board = []
        for row in range(LEN_ROW):
            board.append([])
            for col in range(LEN_COLUMN):
                board[row].append("*")
        for i in range(numOfHints):
            hint = sys.stdin.readline().split()[1:]
            hints.append(tuple(hint))
        for hint in hints:
            row, col, letter = hint
            board[int(row)][int(col)] = letter
            free_row_counts[int(row)] -= 1
            free_col_counts[int(col)] -= 1
            if letter != 'W':
                num_vals_to_add_row[int(row)] -= 1
                num_vals_to_add_col[int(col)] -= 1
        return Board(board, num_vals_to_add_row, num_vals_to_add_col, og_num_vals_to_row, og_num_vals_to_col,
                     free_row_counts, free_col_counts, [], [], [], LEN_ROW, LEN_COLUMN, False)

    def count_boats_to_add(self) -> list:
        num_submarines = 4
        num_cruisers = 3
        num_destroyers = 2
        num_battleships = 1

        for col in range(self.LEN_COLUMN):
            for row in range(self.LEN_ROW):
                letter = self.get_letter(row, col)
                if letter == 'c':
                    num_submarines -= 1
                    self.added_boats.append((row, col, '1', 'h'))
                elif letter == 't':
                    if self.get_letter(row + 1, col) == 'b':
                        num_cruisers -= 1
                        self.added_boats.append((row, col, '2', 'v'))
                    elif self.get_letter(row + 1, col) == 'm':
                        if self.get_letter(row + 2, col) == 'm' \
                                and self.get_letter(row + 3, col) == 'b':
                            num_battleships -= 1
                            self.added_boats.append((row, col, '4', 'v'))
                        elif self.get_letter(row + 2, col) == 'b':
                            num_destroyers -= 1
                            self.added_boats.append((row, col, '3', 'v'))
                elif letter == 'l':
                    if self.get_letter(row, col + 1) == 'r':
                        num_cruisers -= 1
                        self.added_boats.append((row, col, '2', 'h'))
                    elif self.get_letter(row, col + 1) == 'm':
                        if self.get_letter(row, col + 2) == 'm' \
                                and self.get_letter(row, col + 3) == 'r':
                            num_battleships -= 1
                            self.added_boats.append((row, col, '4', 'h'))
                        elif self.get_letter(row, col + 2) == 'r':
                            num_destroyers -= 1
                            self.added_boats.append((row, col, '3', 'h'))

        return [num_submarines, num_cruisers, num_destroyers, num_battleships]

    def get_letter(self, row: int, col: int) -> str:
        """Devolve a letter na respetiva posição do tabuleiro."""
        if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN:
            if self.board[row][col] == '*':
                return "None"
            else:
                return str(self.board[row][col]).lower()
        return "None"

    def process_board(self, redo):
        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):
                letter = self.board[row][col]
                up_letter = self.get_letter(row - 1, col)
                down_letter = self.get_letter(row + 1, col)
                left_letter = self.get_letter(row, col - 1)
                right_letter = self.get_letter(row, col + 1)
                if letter == 'C':
                    self.circle_single_boat_with_water(row, col)
                elif letter == 'T':
                    self.circle_top_of_boat_with_water(row, col)
                    self.add_val_and_circle_with_water(row + 1, col, 'u')
                elif letter == 'M':
                    self.circle_middle_of_boat_with_water(row, col)
                    if up_letter == 'w' or row == 0 or down_letter == 'w' or row == self.LEN_ROW - 1 or \
                            self.has_adjacent_horizontal_val(row, col):
                        self.add_val_and_circle_with_water(row, col - 1, 'u')
                        self.add_val_and_circle_with_water(row, col + 1, 'u')
                    elif left_letter == 'w' or col == 0 or right_letter == 'w' or col == self.LEN_COLUMN - 1 or \
                            self.has_adjacent_vertical_val(row, col):
                        self.add_val_and_circle_with_water(row - 1, col, 'u')
                        self.add_val_and_circle_with_water(row + 1, col, 'u')
                elif letter == 'B':
                    self.circle_bottom_of_boat_with_water(row, col)
                    self.add_val_and_circle_with_water(row - 1, col, 'u')
                elif letter == 'L':
                    self.circle_left_of_boat_with_water(row, col)
                    self.add_val_and_circle_with_water(row, col + 1, 'u')
                elif letter == 'R':
                    self.circle_right_of_boat_with_water(row, col)
                    self.add_val_and_circle_with_water(row, col - 1, 'u')
        if redo:
            self.fill_sections_with_water()
            self.process_board(False)

    def set_value(self, row, col, val):
        """Adiciona uma letra à board numa determinada posição caso já não exista uma letra nessa posição"""
        changed_row = False
        changed_col = False
        if val == 'u':
            self.unknown_vals_pos.append((row, col))
        if self.get_letter(row, col) == "None":
            self.free_col_counts[col] -= 1
            self.free_row_counts[row] -= 1
            if self.num_vals_to_add_row[row] > 0:
                self.num_vals_to_add_row[row] -= 1
                changed_row = True
            if self.num_vals_to_add_col[col] > 0:
                self.num_vals_to_add_col[col] -= 1
                changed_col = True
        self.board[row][col] = val
        # if letter != 'w':
        #   self.try_to_reduce_num_boats_to_add(row, col, letter)
        """       print(changed_col)
        print("COLUNA", self.num_vals_to_add_col)
        print("LINHA", self.num_vals_to_add_row)
        print("FREE COLUNA", self.free_col_counts)
        print("FREE LINHA", self.free_row_counts)
        print("UNKNOWNS", self.unknown_vals_pos)
        print("BOATS TO ADD", self.num_boats_to_add)
        print(self)"""
        self.decipher_unknown_vals()
        if self.num_vals_to_add_row[row] == 0 and changed_row:
            self.fill_row_with_water(row)
        if self.num_vals_to_add_col[col] == 0 and changed_col:
            self.fill_col_with_water(col)

    def set_waters(self, positions_waters):
        for water_pos in positions_waters:
            row, col = water_pos
            if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN and self.get_letter(row, col) == "None":
                self.free_col_counts[col] -= 1
                self.free_row_counts[row] -= 1
                self.board[row][col] = 'w'
                """     print("COLUNA", self.num_vals_to_add_col)
                print("LINHA", self.num_vals_to_add_row)
                print("FREE COLUNA", self.free_col_counts)
                print("FREE LINHA", self.free_row_counts)
                print("UNKNOWNS", self.unknown_vals_pos)
                print(self)"""
                self.decipher_unknown_vals()
        for water_pos in positions_waters:
            row, col = water_pos
            if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN:
                if self.num_vals_to_add_row[row] != 0 and \
                        self.num_vals_to_add_row[row] == self.free_row_counts[row]:
                    self.fill_row_with_unknowns(row)
                if self.num_vals_to_add_col[col] != 0 and \
                        self.num_vals_to_add_col[col] == self.free_col_counts[col]:
                    self.fill_col_with_unknowns(col)

    def fill_sections_with_water(self):
        """Recebe um board, nas linhas e/ou colunas onde o número de
        barcos restantes for zero, a função preenche com água"""
        for row in range(self.LEN_ROW):
            if self.num_vals_to_add_row[row] == 0:
                self.fill_row_with_water(row)
        for col in range(self.LEN_COLUMN):
            if self.num_vals_to_add_col[col] == 0:
                self.fill_col_with_water(col)

    def fill_row_with_water(self, row):
        waters_pos = []
        for col in range(self.LEN_COLUMN):
            if self.get_letter(row, col) == "None":
                waters_pos.append((row, col))
        self.set_waters(waters_pos)

    def fill_col_with_water(self, col):
        waters_pos = []
        for row in range(self.LEN_ROW):
            if self.get_letter(row, col) == "None":
                waters_pos.append((row, col))
        self.set_waters(waters_pos)

    def add_val_and_circle_with_water(self, row, col, val):
        if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN and \
                (self.get_letter(row, col) == "None" or self.get_letter(row, col) == 'u'):
            if self.get_letter(row, col) == 'u' and val == 'u':
                return
            elif val == 'c':
                self.circle_single_boat_with_water(row, col)
            elif val == 't':
                self.circle_top_of_boat_with_water(row, col)
            elif val == 'm':
                self.circle_middle_of_boat_with_water(row, col)
            elif val == 'b':
                self.circle_bottom_of_boat_with_water(row, col)
            elif val == 'l':
                self.circle_left_of_boat_with_water(row, col)
            elif val == 'r':
                self.circle_right_of_boat_with_water(row, col)
            elif val == 'u':
                self.circle_unknown_boat_with_water(row, col)
            self.set_value(row, col, val)

    def is_vertical_isolated_letter(self, row, col):
        up_letter = self.get_letter(row - 1, col)
        down_letter = self.get_letter(row + 1, col)
        return (up_letter == 'w' and down_letter == 'w') or \
            (up_letter == 'w' and row == 9) or \
            (row == 0 and down_letter == 'w')

    def is_horizontal_isolated_letter(self, row, col):
        left_letter = self.get_letter(row, col - 1)
        right_letter = self.get_letter(row, col + 1)
        return (left_letter == 'w' and right_letter == 'w') or \
            (left_letter == 'w' and col == 9) or \
            (right_letter == 'w' and col == 0)

    def replace_unknown_value(self, row, col, val):
        if (row, col) in self.unknown_vals_pos:
            self.unknown_vals_pos.remove((row, col))
        self.add_val_and_circle_with_water(row, col, val)

    def decipher_unknown_vals(self):
        # Copy needed because elements will be removed from the original list
        unknown_vals_pos_copy = self.unknown_vals_pos.copy()
        for pos_unknown in unknown_vals_pos_copy:
            row, col = pos_unknown
            left_letter = self.get_letter(row, col - 1)
            right_letter = self.get_letter(row, col + 1)
            up_letter = self.get_letter(row - 1, col)
            down_letter = self.get_letter(row + 1, col)

            if self.is_horizontal_isolated_letter(row, col) or self.has_adjacent_vertical_val(row, col):
                if self.is_horizontal_isolated_letter(row, col) and self.is_vertical_isolated_letter(row, col):
                    self.replace_unknown_value(row, col, 'c')
                elif down_letter in ['u', 'm', 'b'] and (up_letter == 'w' or row == 0 or
                                                         (up_letter == "None" and self.get_letter(row - 2,
                                                                                                  col) == 'm')):
                    self.replace_unknown_value(row, col, 't')
                elif up_letter in ['u', 'm', 't'] and (down_letter == 'w' or row == self.LEN_ROW - 1 or
                                                       (down_letter == "None" and self.get_letter(row + 2,
                                                                                                  col) == 'm')):
                    self.replace_unknown_value(row, col, 'b')
                elif up_letter in ['u', 'm', 't'] and down_letter in ['u', 'm', 'b']:
                    self.replace_unknown_value(row, col, 'm')
                elif self.get_letter(row - 2, col) == 't':
                    if down_letter == 'w' or row == self.LEN_ROW - 1:
                        self.replace_unknown_value(row, col, 'b')
                    elif down_letter in ['u', 'b']:
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row + 1, col, 'b')
                elif self.get_letter(row + 2, col) == 'b':
                    if up_letter == 'w' or row == 0:
                        self.replace_unknown_value(row, col, 't')
                    elif up_letter in ['u', 't']:
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row - 1, col, 't')

            elif self.is_vertical_isolated_letter(row, col) or self.has_adjacent_horizontal_val(row, col):
                if self.is_vertical_isolated_letter(row, col) and self.is_horizontal_isolated_letter(row, col):
                    self.replace_unknown_value(row, col, 'c')
                elif right_letter in ['u', 'm', 'r'] and (left_letter == 'w' or col == 0 or
                                                          (left_letter == "None" and self.get_letter(row,
                                                                                                     col - 2) == 'm')):
                    self.replace_unknown_value(row, col, 'l')
                elif left_letter in ['u', 'm', 'l'] and (right_letter == 'w' or col == self.LEN_COLUMN - 1 or
                                                         (right_letter == "None" and self.get_letter(row,
                                                                                                     col + 2) == 'm')):
                    self.replace_unknown_value(row, col, 'r')
                elif left_letter in ['u', 'm', 'l'] and right_letter in ['u', 'm', 'r']:
                    self.replace_unknown_value(row, col, 'm')
                elif self.get_letter(row, col - 2) == 'l':
                    if right_letter == 'w' or col == self.LEN_COLUMN - 1:
                        self.replace_unknown_value(row, col, 'r')
                    elif right_letter in ['u', 'r']:
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row, col + 1, 'r')
                elif self.get_letter(row, col + 2) == 'r':
                    if left_letter == 'w' or col == 0:
                        self.replace_unknown_value(row, col, 'l')
                    elif left_letter in ['u', 'l']:
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row, col - 1, 'l')

    def fill_row_with_unknowns(self, row):
        # This is done so the method is not called unnecessarily
        self.num_vals_to_add_row[row] = 0
        for col in range(self.LEN_COLUMN):
            if self.get_letter(row, col) == "None":
                self.add_val_and_circle_with_water(row, col, 'u')

    def fill_col_with_unknowns(self, col):
        # This is done so the method is not called unnecessarily
        self.num_vals_to_add_col[col] = 0
        for row in range(self.LEN_ROW):
            if self.get_letter(row, col) == "None":
                self.add_val_and_circle_with_water(row, col, 'u')

    def circle_single_boat_with_water(self, row, col):
        waters_pos = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1), (row - 1, col - 1),
                      (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]
        self.set_waters(waters_pos)

    def circle_top_of_boat_with_water(self, row, col):
        waters_pos = [(row - 1, col), (row - 1, col - 1), (row - 1, col + 1), (row, col - 1), (row, col + 1),
                      (row + 1, col + 1), (row + 1, col - 1)]
        self.set_waters(waters_pos)

    def circle_middle_of_boat_with_water(self, row, col):
        waters_pos = [(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]
        self.set_waters(waters_pos)

    def circle_bottom_of_boat_with_water(self, row, col):
        waters_pos = [(row + 1, col), (row + 1, col - 1), (row + 1, col + 1), (row, col - 1), (row, col + 1),
                      (row - 1, col + 1), (row - 1, col - 1)]
        self.set_waters(waters_pos)

    def circle_left_of_boat_with_water(self, row, col):
        waters_pos = [(row - 1, col), (row - 1, col - 1), (row - 1, col + 1), (row, col - 1), (row + 1, col),
                      (row + 1, col), (row + 1, col + 1)]
        self.set_waters(waters_pos)

    def circle_right_of_boat_with_water(self, row, col):
        waters_pos = [(row - 1, col), (row - 1, col - 1), (row - 1, col + 1), (row, col + 1), (row + 1, col - 1),
                      (row + 1, col), (row + 1, col + 1)]
        self.set_waters(waters_pos)

    def circle_unknown_boat_with_water(self, row, col):
        waters_pos = [(row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)]
        self.set_waters(waters_pos)

    def copy(self):
        """Creates a copy of the Board."""
        new_board = np.copy(self.board)
        new_num_vals_to_add_row = self.num_vals_to_add_row.copy()
        new_num_vals_to_add_col = self.num_vals_to_add_col.copy()
        new_og_num_vals_to_add_row = self.og_num_vals_to_add_row.copy()
        new_og_num_vals_to_add_col = self.og_num_vals_to_add_col.copy()
        new_free_row_counts = self.free_row_counts.copy()
        new_free_col_counts = self.free_col_counts.copy()
        new_num_boats_to_add = self.num_boats_to_add.copy()
        new_unknown_vals_pos = self.unknown_vals_pos.copy()
        new_added_boats = self.added_boats.copy()

        return Board(new_board, new_num_vals_to_add_row, new_num_vals_to_add_col, new_og_num_vals_to_add_row,
                     new_og_num_vals_to_add_col, new_free_row_counts, new_free_col_counts, new_num_boats_to_add,
                     new_unknown_vals_pos, new_added_boats, self.LEN_ROW, self.LEN_COLUMN, True)

    def is_board_fully_filled(self) -> bool:
        for i in self.free_row_counts:
            if i != 0:
                return False
        for i in self.free_col_counts:
            if i != 0:
                return False
        return True

    def apply_action(self, action):
        row, col, size, direction = action
        if size == '4':
            if direction == "v":
                self.add_val_and_circle_with_water(row, col, "t")
                self.add_val_and_circle_with_water(row + 1, col, "m")
                self.add_val_and_circle_with_water(row + 2, col, "m")
                self.add_val_and_circle_with_water(row + 3, col, "b")
                self.added_boats.append((row, col, '4', 'v'))
            elif direction == "h":
                self.add_val_and_circle_with_water(row, col, "l")
                self.add_val_and_circle_with_water(row, col + 1, "m")
                self.add_val_and_circle_with_water(row, col + 2, "m")
                self.add_val_and_circle_with_water(row, col + 3, "r")
                self.added_boats.append((row, col, '4', 'h'))
        elif size == '3':
            if direction == "v":
                self.add_val_and_circle_with_water(row, col, "t")
                self.add_val_and_circle_with_water(row + 1, col, "m")
                self.add_val_and_circle_with_water(row + 2, col, "b")
                self.added_boats.append((row, col, '3', 'v'))
            elif direction == "h":
                self.add_val_and_circle_with_water(row, col, "l")
                self.add_val_and_circle_with_water(row, col + 1, "m")
                self.add_val_and_circle_with_water(row, col + 2, "r")
                self.added_boats.append((row, col, '3', 'h'))
        elif size == '2':
            if direction == "v":
                self.add_val_and_circle_with_water(row, col, "t")
                self.add_val_and_circle_with_water(row + 1, col, "b")
                self.added_boats.append((row, col, '2', 'v'))
            elif direction == "h":
                self.add_val_and_circle_with_water(row, col, "l")
                self.add_val_and_circle_with_water(row, col + 1, "r")
                self.added_boats.append((row, col, '2', 'h'))
        if size == '1':
            self.add_val_and_circle_with_water(row, col, "c")
            self.added_boats.append((row, col, '1', 'h'))

    def has_boats_with_size_n_to_add(self, n):
        return self.num_boats_to_add[n - 1] > 0

    def is_boat_with_size_n(self, row, col, n, direction):
        if n == '4':
            if direction == 'h' and self.get_letter(row, col) == 'l' and \
                    self.get_letter(row, col + 1) == 'm' and \
                    self.get_letter(row, col + 2) == 'm' and \
                    self.get_letter(row, col + 3) == 'r':
                return True
            elif direction == 'v' and self.get_letter(row, col) == 't' and \
                    self.get_letter(row + 1, col) == 'm' and \
                    self.get_letter(row + 2, col) == 'm' and \
                    self.get_letter(row + 3, col) == 'b':
                return True
        elif n == '3':
            if direction == 'h' and self.get_letter(row, col) == 'l' and \
                    self.get_letter(row, col + 1) == 'm' and \
                    self.get_letter(row, col + 2) == 'r':
                return True
            elif direction == 'v' and self.get_letter(row, col) == 't' and \
                    self.get_letter(row + 1, col) == 'm' and \
                    self.get_letter(row + 2, col) == 'b':
                return True
        elif n == '2':
            if direction == 'h' and self.get_letter(row, col) == 'l' and \
                    self.get_letter(row, col + 1) == 'r':
                return True
            elif direction == 'v' and self.get_letter(row, col) == 't' and \
                    self.get_letter(row + 1, col) == 'b':
                return True
        return False

    """    def num_letters_to_add_to_form_boat(self, row, col, direction):
            counter = 0
            for i in range(4):
                if direction == 'h':
                    if self.get_letter(row, col + i) in ['u', 'None']:
                        counter += 1
                elif direction == 'v':
                    if self.get_letter(row + 1, col) in ['u', 'None']:
                        counter += 1
    """

    def is_value(self, row, col):
        return self.get_letter(row, col) != 'w' and self.get_letter(row, col) != "None"

    def has_adjacent_vertical_val(self, row, col):
        return self.is_value(row - 1, col) or self.is_value(row + 1, col)

    def has_adjacent_horizontal_val(self, row, col):
        return self.is_value(row, col - 1) or self.is_value(row, col + 1)

    def has_adjacent_diagonal_val(self, row, col):
        return self.is_value(row - 1, col - 1) or self.is_value(row - 1, col + 1) or \
            self.is_value(row + 1, col - 1) or self.is_value(row + 1, col + 1)

    def has_adjacent_val(self, row, col):
        return self.has_adjacent_horizontal_val(row, col) or self.has_adjacent_vertical_val(row, col) or \
            self.has_adjacent_diagonal_val(row, col)

    def all_boats_are_valid(self):
        for boat in self.added_boats:
            row, col, size, direction = boat
            if self.boat_has_invalid_adjacent_val(row, col, size, direction):
                return False
        return True

    def boat_has_invalid_adjacent_val(self, row, col, size, direction):
        if size == '4':
            if direction == 'h':
                return self.is_value(row, col - 1) or self.has_adjacent_vertical_val(row, col) or \
                    self.has_adjacent_diagonal_val(row, col) or self.has_adjacent_diagonal_val(row, col + 3) or \
                    self.has_adjacent_vertical_val(row, col + 3) or self.is_value(row, col + 4)
            elif direction == 'v':
                return self.is_value(row - 1, col) or self.has_adjacent_horizontal_val(row, col) or \
                    self.has_adjacent_diagonal_val(row, col) or self.has_adjacent_diagonal_val(row + 3, col) or \
                    self.has_adjacent_horizontal_val(row + 3, col) or self.is_value(row + 4, col)
        elif size == '3':
            if direction == 'h':
                return self.is_value(row, col - 1) or self.has_adjacent_vertical_val(row, col) or \
                    self.has_adjacent_diagonal_val(row, col) or self.has_adjacent_diagonal_val(row, col + 2) or \
                    self.has_adjacent_vertical_val(row, col + 2) or self.is_value(row, col + 3)
            elif direction == 'v':
                return self.is_value(row - 1, col) or self.has_adjacent_horizontal_val(row, col) or \
                    self.has_adjacent_diagonal_val(row, col) or self.has_adjacent_diagonal_val(row + 2, col) or \
                    self.has_adjacent_horizontal_val(row + 2, col) or self.is_value(row + 3, col)
        elif size == '2':
            if direction == 'h':
                return self.is_value(row, col - 1) or self.has_adjacent_vertical_val(row, col) or \
                    self.has_adjacent_diagonal_val(row, col) or self.has_adjacent_vertical_val(row, col + 2) or \
                    self.is_value(row, col + 2)
            elif direction == 'v':
                return self.is_value(row - 1, col) or self.has_adjacent_horizontal_val(row, col) or \
                    self.has_adjacent_diagonal_val(row, col) or self.has_adjacent_horizontal_val(row + 2, col) or \
                    self.is_value(row + 2, col)

    def num_vals_needed_to_add(self, row, col, size, direction):
        counter = 0
        for i in range(int(size)):
            if direction == 'h':
                if self.get_letter(row, col + i) == 'None':
                    counter += 1
            elif direction == 'v':
                if self.get_letter(row + i, col) == "None":
                    counter += 1
        return counter

    def biggest_boat_to_add_positions(self):
        biggest_boat_to_add_pos = []
        if self.has_boats_with_size_n_to_add(4):
            for row in range(self.LEN_ROW):
                if self.num_vals_to_add_row[row] > 0 and self.og_num_vals_to_add_row[row] > 3:
                    for col in range(self.LEN_COLUMN - 3):
                        if self.get_letter(row, col) in ['l', 'u', "None"] and \
                                self.get_letter(row, col + 1) in ['m', 'u', "None"] and \
                                self.get_letter(row, col + 2) in ['m', 'u', 'None'] and \
                                self.get_letter(row, col + 3) in ['r', 'u', 'None'] and \
                                self.num_vals_needed_to_add(row, col, '4', 'h') <= self.num_vals_to_add_row[row] and not \
                                self.boat_has_invalid_adjacent_val(row, col, '4,', 'h') and not \
                                self.is_boat_with_size_n(row, col, '4', 'h'):
                            biggest_boat_to_add_pos.append((row, col, '4', 'h'))
            for col in range(self.LEN_COLUMN):
                if self.num_vals_to_add_col[col] > 0 and self.og_num_vals_to_add_col[col] > 3:
                    for row in range(self.LEN_ROW - 3):
                        if self.get_letter(row, col) in ['t', 'u', "None"] and \
                                self.get_letter(row + 1, col) in ['m', 'u', "None"] and \
                                self.get_letter(row + 2, col) in ['m', 'u', 'None'] and \
                                self.get_letter(row + 3, col) in ['b', 'u', 'None'] and \
                                self.num_vals_needed_to_add(row, col, '4', 'v') <= self.num_vals_to_add_col[col] and not \
                                self.boat_has_invalid_adjacent_val(row, col, '4', 'v') and not \
                                self.is_boat_with_size_n(row, col, '4', 'v'):
                            biggest_boat_to_add_pos.append((row, col, '4', 'v'))

        elif self.has_boats_with_size_n_to_add(3):
            for row in range(self.LEN_ROW):
                if self.num_vals_to_add_row[row] > 0 and self.og_num_vals_to_add_row[row] > 2:
                    for col in range(self.LEN_COLUMN - 2):
                        if self.get_letter(row, col) in ['l', 'u', "None"] and \
                                self.get_letter(row, col + 1) in ['m', 'u', "None"] and \
                                self.get_letter(row, col + 2) in ['r', 'u', 'None'] and \
                                self.num_vals_needed_to_add(row, col, '3', 'h') <= self.num_vals_to_add_row[row] and not \
                                self.boat_has_invalid_adjacent_val(row, col, '3', 'h') and not \
                                self.is_boat_with_size_n(row, col, '3', 'h'):
                            biggest_boat_to_add_pos.append((row, col, '3', 'h'))
            for col in range(self.LEN_COLUMN):
                if self.num_vals_to_add_col[col] > 0 and self.og_num_vals_to_add_col[col] > 2:
                    for row in range(self.LEN_ROW - 2):
                        if self.get_letter(row, col) in ['t', 'u', "None"] and \
                                self.get_letter(row + 1, col) in ['m', 'u', "None"] and \
                                self.get_letter(row + 2, col) in ['b', 'u', 'None'] and \
                                self.num_vals_needed_to_add(row, col, '3', 'v') <= self.num_vals_to_add_col[col] and not \
                                self.boat_has_invalid_adjacent_val(row, col, '3', 'v') and not \
                                self.is_boat_with_size_n(row, col, '3', 'v'):
                            biggest_boat_to_add_pos.append((row, col, '3', 'v'))

        elif self.has_boats_with_size_n_to_add(2):
            for row in range(self.LEN_ROW):
                if self.num_vals_to_add_row[row] > 0 and self.og_num_vals_to_add_row[row] > 1:
                    for col in range(self.LEN_COLUMN - 1):
                        if self.get_letter(row, col) in ['l', 'u', "None"] and \
                                self.get_letter(row, col + 1) in ['r', 'u', 'None'] and \
                                self.num_vals_needed_to_add(row, col, '2', 'h') <= self.num_vals_to_add_row[row] and not \
                                self.boat_has_invalid_adjacent_val(row, col, '2', 'h') and not \
                                self.is_boat_with_size_n(row, col, '2', 'h'):
                            biggest_boat_to_add_pos.append((row, col, '2', 'h'))
            for col in range(self.LEN_COLUMN):
                if self.num_vals_to_add_col[col] > 0 and self.og_num_vals_to_add_col[col] > 1:
                    for row in range(self.LEN_ROW - 1):
                        if self.get_letter(row, col) in ['t', 'u', "None"] and \
                                self.get_letter(row + 1, col) in ['b', 'u', 'None'] and \
                                self.num_vals_needed_to_add(row, col, '2', 'v') <= self.num_vals_to_add_col[col] and not \
                                self.boat_has_invalid_adjacent_val(row, col, '2', 'v') and not \
                                self.is_boat_with_size_n(row, col, '2', 'v'):
                            biggest_boat_to_add_pos.append((row, col, '2', 'v'))

        elif self.has_boats_with_size_n_to_add(1):
            for row in range(self.LEN_ROW):
                if self.num_vals_to_add_row[row] > 0:
                    for col in range(self.LEN_COLUMN):
                        if self.get_letter(row, col) in ['u', "None"] and not \
                                self.has_adjacent_val(row, col):
                            # indifferent for h and v
                            biggest_boat_to_add_pos.append((row, col, '1', 'h'))
        return biggest_boat_to_add_pos

    def add_char_to_print(self, row, col, board_to_print):
        if self.board[row][col] == 'w':
            board_to_print += '.'
            # board_to_print += ' '
        else:
            board_to_print += self.board[row][col]
            # board_to_print += ' '
        return board_to_print

    def __repr__(self):
        board_to_print = ''
        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):
                if col != self.LEN_COLUMN - 1:
                    board_to_print = self.add_char_to_print(row, col, board_to_print)
                else:
                    board_to_print = self.add_char_to_print(row, col, board_to_print)
                    if row != self.LEN_ROW - 1:
                        board_to_print += '\n'
        return board_to_print


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        state = BimaruState(board)
        super().__init__(state)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        """    print("COLUNA", state.board.num_vals_to_add_col)
        print("LINHA", state.board.num_vals_to_add_row)
        print("FREE COLUNA", state.board.free_col_counts)
        print("FREE LINHA", state.board.free_row_counts)
        print("ACTIONS:", state.board.biggest_boat_to_add_positions())
        print("BOATS", state.board.num_boats_to_add)
        print(state.board)"""
        return state.board.biggest_boat_to_add_positions()

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # print(state.state_id, action)
        new_board = state.board.copy()
        new_board.apply_action(action)
        # print("NEW BOARD:")
        # new_board.print()
        return BimaruState(new_board)

    def goal_test(self, state: BimaruState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""

        state.board.num_boats_to_add = state.board.count_boats_to_add()
        return state.board.is_board_fully_filled() and state.board.num_boats_to_add == [0, 0, 0, 0] and \
            len(state.board.unknown_vals_pos) == 0 and state.board.all_boats_are_valid()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO


if __name__ == "__main__":
    # Ler grelha do ficheiro 'i1.txt' (Figura 1):
    # $ python3 bimaru.py < i1.txt
    board = Board.parse_instance()
    # print(board)
    state = BimaruState(board)
    problem = Bimaru(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    """    num_vals_row = [0 for _ in range(10)]
    num_vals_col = [0 for _ in range(10)]
    for col in range(10):
        for row in range(10):
            if goal_node.state.board.is_value(row, col):
                num_vals_col[col] += 1
    for row in range(10):
        for col in range(10):
            if goal_node.state.board.is_value(row, col):
                num_vals_row[row] += 1
    print("Numero de valores em linhas:", num_vals_row)
    print("Numero de valores em colunas:", num_vals_col)
    print("Numero de barcos", goal_node.state.board.num_boats_to_add)
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:")"""
    print(goal_node.state.board)
