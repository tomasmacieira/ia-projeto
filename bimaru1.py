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
        return self.id > other.id


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, board, values_to_add_row_counts, values_to_add_col_counts, free_row_counts, free_col_counts,
                 len_row, len_column, num_boats_to_add, isCopy):
        self.board = board
        self.values_to_add_row_counts = values_to_add_row_counts
        self.values_to_add_col_counts = values_to_add_col_counts
        self.LEN_ROW = len_row
        self.LEN_COLUMN = len_column
        self.free_row_counts = free_row_counts
        self.free_col_counts = free_col_counts
        self.unknown_values_positions = []
        if isCopy:
            self.num_boats_to_add = num_boats_to_add
        else:
            self.num_boats_to_add = self.count_boats_to_add()
            self.process_board()

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
                elif letter == 't':
                    if self.get_letter(row + 1, col) == 'b':
                        num_cruisers -= 1
                        row -= 1
                    elif self.get_letter(row + 1, col) == 'm':
                        if self.get_letter(row + 2, col) == 'm' \
                                and self.get_letter(row + 3, col) == 'b':
                            num_battleships -= 1
                            row += 3
                        elif self.get_letter(row + 2, col) == 'b':
                            num_destroyers -= 1
                            row += 2
                elif letter == 'l':
                    if self.get_letter(row, col + 1) == 'r':
                        num_cruisers -= 1
                    elif self.get_letter(row, col + 1) == 'm':
                        if self.get_letter(row, col + 2) == 'm' \
                                and self.get_letter(row, col + 3) == 'r':
                            num_battleships -= 1
                        elif self.get_letter(row, col + 2) == 'r':
                            num_destroyers -= 1

        return [num_submarines, num_cruisers, num_destroyers, num_battleships]

    def get_letter(self, row: int, col: int) -> str:
        """Devolve o letteror na respetiva posição do tabuleiro."""
        if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN:
            if self.board[row][col] == '*':
                return "None"
            else:
                return str(self.board[row][col]).lower()
        return "None"

    def get_horizontal_values(self, row, col):
        return (self.get_letter(row, col - 1), self.get_letter(row, col + 1))
    
    def get_vertical_values(self, row, col):
        return (self.get_letter(row - 1, col), self.get_letter(row + 1, col))
    
    def get_diagonal_values(self, row, col):
        return (
            self.get_letter(row - 1, col - 1),
            self.get_letter(row + 1, col - 1),
            self.get_letter(row - 1, col + 1),
            self.get_letter(row + 1, col + 1)
        )

    def process_board(self):
        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):
                letter = self.board[row][col]
                if letter == 'C':
                    self.circle_single_boat_with_water(row, col)
                elif letter == 'T':
                    self.circle_top_of_boat_with_water(row, col)
                elif letter == 'M':
                    self.circle_middle_of_boat_with_water(row, col)
                elif letter == 'B':
                    self.circle_bottom_of_boat_with_water(row, col)
                elif letter == 'L':
                    self.circle_left_of_boat_with_water(row, col)
                elif letter == 'R':
                    self.circle_right_of_boat_with_water(row, col)
        self.print()
        self.fill_sections_with_water()
        #self.decipher_unknown_values()

    def fill_sections_with_water(self):
        """Recebe um board, nas linhas e/ou colunas onde o número de
        barcos restantes for zero, a função preenche com água"""
        for row in range(self.LEN_ROW):
            if self.values_to_add_row_counts[row] == 0:
                self.fill_row_with_water(row)

        for col in range(self.LEN_COLUMN):
            if self.values_to_add_col_counts[col] == 0:
                self.fill_col_with_water(col)

    def fill_row_with_water(self, row):
        for col in range(self.LEN_COLUMN):
            if self.get_letter(row, col) == "None":
                self.set_letter(row, col, 'w')

    def fill_col_with_water(self, col):
        for row in range(self.LEN_ROW):
            if self.get_letter(row, col) == "None":
                self.set_letter(row, col, 'w')

    def set_letter(self, row, col, letter):
        """Adiciona uma letra à board numa determinada posição caso já não exista um letra nessa posição"""
        if 0 <= row < self.LEN_ROW and 0 <= col < self.LEN_COLUMN and \
                (self.get_letter(row, col) == "None" or self.get_letter(row, col) == 'u'):
            if self.get_letter(row, col) == 'None':
                self.free_col_counts[col] -= 1
                self.free_row_counts[row] -= 1
            self.board[row][col] = letter
            if letter != 'w':
                if self.values_to_add_row_counts[row] > 0:
                    self.values_to_add_row_counts[row] -= 1
                    if self.values_to_add_row_counts[row] == 0:
                        self.fill_row_with_water(row)
                if self.values_to_add_col_counts[col] > 0:
                    self.values_to_add_col_counts[col] -= 1
                    if self.values_to_add_col_counts[col] == 0:
                        self.fill_col_with_water(col)
            if self.values_to_add_row_counts[row] != 0 and \
                    self.values_to_add_row_counts[row] == self.free_row_counts[row]:
                self.fill_row_with_values(row)
            if self.values_to_add_col_counts[col] != 0 and \
                    self.values_to_add_col_counts[col] == self.free_col_counts[col]:
                self.fill_col_with_values(col)

    def is_vertical_isolated_letter(self, row, col):
        up_letter = self.get_letter(row - 1, col)
        down_letter = self.get_letter(row + 1, col)
        return (up_letter == 'w' and down_letter == 'w') or \
            (up_letter == 'w' and row + 1 == 10) or \
            (row - 1 == -1 and down_letter == 'w')

    def is_horizontal_isolated_letter(self, row, col):
        left_letter = self.get_letter(row, col - 1)
        right_letter = self.get_letter(row, col + 1)
        return (left_letter == 'w' and right_letter == 'w') or \
            (left_letter == 'w' and col + 1 == 10) or \
            (right_letter == 'w' and col - 1 == -1)

    def has_adjacent_vertical_values(self, row, col):
        return (self.get_letter(row - 1, col) != 'w' and self.get_letter(row - 1, col) != 'None') or \
            (self.get_letter(row + 1, col) != 'w' and self.get_letter(row + 1, col) != 'None')

    def has_adjacent_horizontal_values(self, row, col):
        return (self.get_letter(row, col - 1) != 'w' and self.get_letter(row, col - 1) != 'None') or \
            (self.get_letter(row, col + 1) != 'w' and self.get_letter(row, col + 1) != 'None')

    def replace_unknown_value(self, row, col, val):
        self.add_value_and_circle_with_water(row, col, val)
        if (row, col) in self.unknown_values_positions:
            self.unknown_values_positions.remove((row, col))

    def decipher_unknown_values(self):
        # Copy needed because elements will be removed from the original list
        unknown_values_positions_copy = self.unknown_values_positions.copy()
        for pos_unknown in unknown_values_positions_copy:
            row, col = pos_unknown
            left_letter = self.get_letter(row, col - 1)
            right_letter = self.get_letter(row, col + 1)
            up_letter = self.get_letter(row - 1, col)
            down_letter = self.get_letter(row + 1, col)

            if self.is_horizontal_isolated_letter(row, col) or self.has_adjacent_vertical_values(row, col):
                if self.is_vertical_isolated_letter(row, col) and self.is_horizontal_isolated_letter(row, col):
                    self.replace_unknown_value(row, col, 'c')
                elif up_letter == 'w' or row == 0:
                    self.replace_unknown_value(row, col, 't')
                elif down_letter == 'w' or row == self.LEN_ROW - 1:
                    self.replace_unknown_value(row, col, 'b')
                elif up_letter in ['u', 't']:
                    if (self.get_letter(row - 2, col) == 'w' and down_letter == 'w') or \
                            (row - 2 == -1 and down_letter == 'w') or \
                            (self.get_letter(row - 2, col) == 'w' and row == self.LEN_ROW - 1):
                        self.replace_unknown_value(row, col, 'b')
                    elif down_letter in ['u', 'b', 'm']:
                        self.replace_unknown_value(row, col, 'm')
                elif down_letter in ['u', 'b']:
                    if (self.get_letter(row + 2, col) == 'w' and up_letter == 'w') or \
                            (row + 2 == 10 and up_letter == 'w') or \
                            (self.get_letter(row + 2, col) == 'w' and row == 0):
                        self.replace_unknown_value(row, col, 't')
                    elif up_letter in ['u', 'm']:
                        self.replace_unknown_value(row, col, 'm')
                elif self.get_letter(row - 2, col) == 't':
                    self.replace_unknown_value(row - 1, col, 'm')
                    if down_letter == 'w' or row == self.LEN_ROW - 1:
                        self.replace_unknown_value(row, col, 'b')
                    elif down_letter in ['b', 'u']:
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row + 1, col, 'b')
                elif self.get_letter(row + 2, col) == 'b':
                    self.replace_unknown_value(row + 1, col, 'm')
                    if up_letter == 'w' or row == 0:
                        self.replace_unknown_value(row, col, 't')
                    elif up_letter in ['t', 'u']:
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row - 1, col, 't')

            elif self.is_vertical_isolated_letter(row, col) or self.has_adjacent_horizontal_values(row, col):
                if self.is_horizontal_isolated_letter(row, col) and self.is_vertical_isolated_letter(row, col):
                    self.replace_unknown_value(row, col, 'c')
                elif left_letter == 'w' or col == 0:
                    self.replace_unknown_value(row, col, 'l')
                elif right_letter == 'w' or col == self.LEN_COLUMN - 1:
                    self.replace_unknown_value(row, col, 'r')
                elif left_letter in ['u', 'l']:
                    if (self.get_letter(row, col - 2) == 'w' and right_letter == 'w') or \
                            (col - 2 == -1 and right_letter == 'w') or \
                            (self.get_letter(row, col - 2) == 'w' and col == self.LEN_COLUMN - 1):
                        self.replace_unknown_value(row, col, 'r')
                    elif right_letter in ['m', 'r', 'u']:
                        self.replace_unknown_value(row, col, 'm')
                elif right_letter in ['u', 'r']:
                    if (self.get_letter(row, col + 2) == 'w' and left_letter == 'w') or \
                            (col + 2 == 10 and left_letter == 'w') or \
                            (self.get_letter(row, col + 2) == 'w' and col == 0):
                        self.replace_unknown_value(row, col, 'l')
                    elif left_letter in ['u', 'm']:
                        self.replace_unknown_value(row, col, 'm')
                elif self.get_letter(row, col - 2) == 'l':
                    self.replace_unknown_value(row, col - 1, 'm')
                    if right_letter == 'w' or col == self.LEN_COLUMN - 1:
                        self.replace_unknown_value(row, col, 'r')
                    elif right_letter == 'r' or right_letter == 'u':
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row, col + 1, 'r')
                elif self.get_letter(row, col + 2) == 'r':
                    self.replace_unknown_value(row, col + 1, 'm')
                    if left_letter == 'w' or col == 0:
                        self.replace_unknown_value(row, col, 'l')
                    elif left_letter == 'l' or left_letter == 'u':
                        self.replace_unknown_value(row, col, 'm')
                        self.replace_unknown_value(row, col - 1, 'l')

    def space_available(self, row, col, size, direction):
        """Function decides if there is space available for a
        boat of size size following the direction giving, ex:
        boat with size 4, horizontal starting at (0,0)"""

        #Vertical
        if direction == "v":
            num_of_pieces = self.values_to_add_col_counts[col]
            pieces_in_row = 0
            for i in range(1, size):
                if i == size - 1:
                    if all(value in ("b","u") for value in self.get_letter(row + i, col)):
                        pieces_in_row += 1  
                if i < size - 1:
                    if all(value in ("m","u") for value in self.get_letter(row + i, col)):
                        pieces_in_row += 1
            if num_of_pieces + pieces_in_row < 3:
                return False
            if num_of_pieces <= 3 and pieces_in_row == 0:
                return False
            return True
        
        #Horizontal
        if direction == "h":
            num_of_pieces = self.values_to_add_row_counts[row]
            pieces_in_row = 0
            for i in range(1, size):
                if i == size - 1:
                    if all(value in ("r","u") for value in self.get_letter(row, col + i)):
                        pieces_in_row += 1  
                if i < size - 1:
                    if all(value in ("m","u") for value in self.get_letter(row, col + i)):
                        pieces_in_row += 1
            if num_of_pieces + pieces_in_row < 3:
                return False
            if num_of_pieces <= 3 and pieces_in_row == 0:
                return False
            return True

    def check_value_border(self, row, col, direction):

        val = self.get_letter(row, col)

        if val == "c":
            return all(value in ("None", "w") for value in self.get_horizontal_values(row, col)) and \
                all(value in ("None", "w") for value in self.get_vertical_values(row, col)) and \
                all(value in ("None", "w") for value in self.get_diagonal_values(row, col))
        
        if val == "t":
            return all(value in ("None", "w") for value in (self.get_letter(row - 1, col),)) and \
                all(value in ("None", "w") for value in self.get_horizontal_values(row, col)) and \
                all(value in ("None", "w") for value in self.get_diagonal_values(row, col))


        if val == "m" or val == "u" or val == "None":
            if direction == "v":
                return all(value in ("None", "w") for value in self.get_horizontal_values(row, col)) and \
                    all(value in ("None", "w") for value in self.get_diagonal_values(row, col))

            if direction == "h":
                return all(value in ("None", "w") for value in self.get_vertical_values(row, col)) and \
                    all(value in ("None", "w") for value in self.get_diagonal_values(row, col))

        if val == "b":
            return self.get_letter(row + 1, col) == "None" and \
                self.get_horizontal_values(row, col) == ("None", "None") and \
                self.get_diagonal_values(row, col) == ("None", "None", "None", "None") 

        if val == "l":
            return self.get_letter(row, col - 1) == "None" and \
                self.get_vertical_values(row, col) == ("None", "None") and \
                self.get_diagonal_values(row, col) == ("None", "None", "None", "None")

        if val == "r":
            return self.get_letter(row, col + 1) == "None" and \
                self.get_vertical_values(row, col) == ("None", "None") and \
                self.get_diagonal_values(row, col) == ("None", "None", "None", "None")

    def biggest_boat_positions(self):

        biggest_boat_pos = []
        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):

                #Search positions for a battleship
                if self.num_boats_to_add[3] > 0 and 1 + 1 == 3:
                    BOAT_SIZE = 4   
                    if row < 7 and self.space_available(row,col,BOAT_SIZE,"v") and self.check_value_border(row,col,"v") and \
                        self.get_letter(row - 1, col) != "t" and self.values_to_add_row_counts[row] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row + i, col, "v") and self.values_to_add_row_counts[row + i] != 0:
                                checks += 1
                        if checks == 3:
                            biggest_boat_pos.append((row,col,4,"v"))
                    
                    #Horizontally:
                    if col < 7 and self.space_available(row,col,BOAT_SIZE,"h") and self.check_value_border(row,col,"h") and \
                        self.get_letter(row, col - 1) != "l" and self.values_to_add_col_counts[col] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row, col + i, "h") and self.values_to_add_col_counts[col + i] != 0:
                                checks += 1
                        if checks == 3:
                            biggest_boat_pos.append((row,col,4,"h"))

                 #Search positions for a cruiser
                elif self.num_boats_to_add[2] > 0:
                    BOAT_SIZE = 3   

                    if row == 7 and col == 0:
                        print(self.values_to_add_row_counts[row + 1] != 0, self.values_to_add_row_counts[8])

                    if row < 8 and self.space_available(row,col,BOAT_SIZE,"v") and self.check_value_border(row,col,"v") and \
                        self.get_letter(row - 1, col) != "t" and self.values_to_add_row_counts[row] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row + i, col, "v") and self.values_to_add_row_counts[row + i] != 0:
                                checks += 1
                        if checks == 2:
                            biggest_boat_pos.append((row,col,3,"v"))
                    
                    #Horizontally:
                    if col < 8 and self.space_available(row,col,BOAT_SIZE,"h") and self.check_value_border(row,col,"h") and \
                        self.get_letter(row, col - 1) != "l" and self.values_to_add_col_counts[col] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row, col + i, "h") and self.values_to_add_col_counts[col + i] != 0:
                                checks += 1
                        if checks == 2:
                            biggest_boat_pos.append((row,col,3,"h"))
                
                 #Search positions for a destroyer
                elif self.num_boats_to_add[1] > 0:
                    BOAT_SIZE = 2   
                    if row < 9 and self.space_available(row,col,BOAT_SIZE,"v") and self.check_value_border(row,col,"v") and \
                        self.get_letter(row - 1, col) != "t" and self.values_to_add_row_counts[row] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row + i, col, "v") and self.values_to_add_row_counts[row + i] != 0:
                                checks += 1
                        if checks == 1:
                            biggest_boat_pos.append((row,col,2,"v"))
                    
                    #Horizontally:
                    if col < 9 and self.space_available(row,col,BOAT_SIZE,"h") and self.check_value_border(row,col,"h") and \
                        self.get_letter(row, col - 1) != "l" and self.values_to_add_col_counts[col] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row, col + i, "h") and self.values_to_add_col_counts[col + i] != 0:
                                checks += 1
                        if checks == 1:
                            biggest_boat_pos.append((row,col,2,"h"))

                #Search positions for a submarine
                elif self.num_boats_to_add[0] > 0:
                    BOAT_SIZE = 1   
                    if row < 10 and self.space_available(row,col,BOAT_SIZE,"v") and self.check_value_border(row,col,"v") and \
                        self.get_letter(row - 1, col) != "t" and self.values_to_add_row_counts[row] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row + i, col, "v") and self.values_to_add_row_counts[row + i] != 0:
                                checks += 1
                        if checks == 0:
                            biggest_boat_pos.append((row,col,1,"v"))
                    
                    #Horizontally:
                    if col < 10 and self.space_available(row,col,BOAT_SIZE,"h") and self.check_value_border(row,col,"h") and \
                        self.get_letter(row, col - 1) != "l" and self.values_to_add_col_counts[col] != 0:
                        checks = 0
                        for i in range(1,BOAT_SIZE):
                            if self.check_value_border(row, col + i, "h") and self.values_to_add_col_counts[col + i] != 0:
                                checks += 1
                        if checks == 0:
                            biggest_boat_pos.append((row,col,1,"h"))

        return biggest_boat_pos

    def apply_action(self, action):
        row, col, type, direction = action

        #Put battleship
        if type == 4:
            if direction == "v":
                self.add_value_and_circle_with_water(row, col , "t")
                self.add_value_and_circle_with_water(row + 1, col , "m")
                self.add_value_and_circle_with_water(row + 2, col , "m")
                self.add_value_and_circle_with_water(row + 3, col , "b")
            elif  direction == "h":
                self.add_value_and_circle_with_water(row, col, "l")
                self.add_value_and_circle_with_water(row, col + 1 , "m")
                self.add_value_and_circle_with_water(row, col + 2, "m")
                self.add_value_and_circle_with_water(row, col + 3, "r")
        
        if type == 3:
            if direction == "v":
                self.add_value_and_circle_with_water(row, col , "t")
                self.add_value_and_circle_with_water(row + 1, col , "m")
                self.add_value_and_circle_with_water(row + 2, col , "b")
            if direction == "h":
                self.add_value_and_circle_with_water(row, col , "l")
                self.add_value_and_circle_with_water(row, col + 1 , "m")
                self.add_value_and_circle_with_water(row, col + 2, "r")
        
        if type == 2:
            if direction == "v":
                self.add_value_and_circle_with_water(row, col , "t")
                self.add_value_and_circle_with_water(row + 1, col , "b")
            if direction == "h":
                self.add_value_and_circle_with_water(row, col + 1 , "l")
                self.add_value_and_circle_with_water(row, col + 2, "r")
        
        if type == 1:
            self.add_value_and_circle_with_water((row, col, "c"))

    def fill_row_with_values(self, row):
        # This is does so the method is not called unnecessarily
        self.values_to_add_row_counts[row] = 0
        for col in range(self.LEN_COLUMN):
            letter = self.get_letter(row, col)
            left_letter = self.get_letter(row, col - 1)
            right_letter = self.get_letter(row, col + 1)

            if letter == "None":
                if self.is_horizontal_isolated_letter(row, col):
                    if self.is_vertical_isolated_letter(row, col):
                        self.add_value_and_circle_with_water(row, col, 'c')
                    else:
                        self.add_value_and_circle_with_water(row, col, 'u')
                elif left_letter == 'w':
                    self.add_value_and_circle_with_water(row, col, 'l')
                elif left_letter == 'l' and right_letter == 'r':
                    self.add_value_and_circle_with_water(row, col, 'm')
                elif left_letter == 'l':
                    if right_letter == 'w':
                        self.add_value_and_circle_with_water(row, col, 'r')
                    elif right_letter == "None":
                        self.add_value_and_circle_with_water(row, col, 'm')
                elif left_letter == 'm':
                    if (right_letter == 'w' or col + 1 == 10) or \
                            (right_letter == 'r' or right_letter == "None"):
                        self.add_value_and_circle_with_water(row, col, 'r')
                    else:
                        self.add_value_and_circle_with_water(row, col, 'm')
                else:
                    self.add_value_and_circle_with_water(row, col, 'u')

    def fill_col_with_values(self, col):
        # This is does so the method is not called unnecessarily
        self.values_to_add_col_counts[col] = 0
        for row in range(self.LEN_ROW):
            letter = self.get_letter(row, col)
            up_letter = self.get_letter(row - 1, col)
            down_letter = self.get_letter(row + 1, col)
            if letter == "None":
                if self.is_vertical_isolated_letter(row, col):
                    if self.is_horizontal_isolated_letter(row, col):
                        self.add_value_and_circle_with_water(row, col, 'c')
                    else:
                        self.add_value_and_circle_with_water(row, col, 'u')
                elif up_letter == 'w':
                    self.add_value_and_circle_with_water(row, col, 't')
                elif up_letter == 't' and down_letter == 'b':
                    self.add_value_and_circle_with_water(row, col, 'm')
                elif up_letter == 't':
                    if down_letter == 'w':
                        self.add_value_and_circle_with_water(row, col, 'b')
                    elif down_letter == "None":
                        self.add_value_and_circle_with_water(row, col, 'm')
                elif up_letter == 'm':
                    if (down_letter == 'w' or row + 1 == 10) or \
                            (down_letter == 'b' or down_letter == "None"):
                        self.add_value_and_circle_with_water(row, col, 'b')
                    else:
                        self.add_value_and_circle_with_water(row, col, 'm')
                else:
                    self.add_value_and_circle_with_water(row, col, 'u')

    def add_value_and_circle_with_water(self, row, col, val):
        if val != "u":
            self.set_letter(row, col, val)

        if val == 'c':
            self.circle_single_boat_with_water(row, col)
            self.reduce_num_of_boats_to_add_with_size_n(1)
        elif val == 't':
            self.circle_top_of_boat_with_water(row, col)
            if self.get_letter(row + 1, col) == 'b':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_letter(row + 1, col) == 'm':
                if self.get_letter(row + 2, col) == 'b':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_letter(row + 2, col) == 'm' and self.get_letter(row + 3, col) == 'b':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif val == 'm':
            if self.get_letter(row - 1, col) == 't' and self.get_letter(row + 1, col) == 'b':
                self.reduce_num_of_boats_to_add_with_size_n(3)
            elif (self.get_letter(row - 1, col) == 'm' and self.get_letter(row - 2, col) == 't' and
                  self.get_letter(row + 1, col) == 'b') or \
                    (self.get_letter(row + 1, col) == 'm' and self.get_letter(row - 1, col) == 't' and
                     self.get_letter(row + 2, col) == 'b'):
                self.reduce_num_of_boats_to_add_with_size_n(4)
            elif self.get_letter(row, col - 1) == 'l' and self.get_letter(row, col + 1) == 'r':
                self.reduce_num_of_boats_to_add_with_size_n(3)
            elif (self.get_letter(row, col - 1) == 'm' and self.get_letter(row, col - 2) == 'l' and
                  self.get_letter(row, col + 1) == 'r') or \
                    (self.get_letter(row, col + 1) == 'm' and self.get_letter(row, col - 1) == 'l' and
                     self.get_letter(row, col + 1) == 'r'):
                self.reduce_num_of_boats_to_add_with_size_n(4)
        elif val == 'b':
            self.circle_bottom_of_boat_with_water(row, col)
            if self.get_letter(row - 1, col) == 't':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_letter(row - 1, col) == 'm':
                if self.get_letter(row - 2, col) == 't':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_letter(row - 2, col) == 'm' and self.get_letter(row - 3, col) == 't':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif val == 'l':
            self.circle_left_of_boat_with_water(row, col)
            if self.get_letter(row, col + 1) == 'r':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_letter(row, col + 1) == 'm':
                if self.get_letter(row, col + 2) == 'r':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_letter(row, col + 2) == 'm' and self.get_letter(row, col + 3) == 'r':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif val == 'r':
            self.circle_right_of_boat_with_water(row, col)
            if self.get_letter(row, col - 1) == 'l':
                self.reduce_num_of_boats_to_add_with_size_n(2)
            elif self.get_letter(row, col - 1) == 'm':
                if self.get_letter(row, col - 2) == 'l':
                    self.reduce_num_of_boats_to_add_with_size_n(3)
                elif self.get_letter(row, col - 2) == 'm' and self.get_letter(row, col - 3) == 'l':
                    self.reduce_num_of_boats_to_add_with_size_n(4)
        elif val == 'u':
            return
            #self.circle_unknown_boat_with_water(row, col)
            #self.unknown_values_positions.append((row, col))

    def reduce_num_of_boats_to_add_with_size_n(self, n: int):
        self.num_boats_to_add[n - 1] -= 1

    def circle_single_boat_with_water(self, row, col):
        self.set_letter(row - 1, col, "w")
        self.set_letter(row + 1, col, "w")
        self.set_letter(row, col - 1, "w")
        self.set_letter(row, col + 1, "w")
        self.set_letter(row - 1, col - 1, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row + 1, col - 1, "w")
        self.set_letter(row + 1, col + 1, "w")

    def circle_top_of_boat_with_water(self, row, col):
        self.set_letter(row - 1, col, "w")
        self.set_letter(row - 1, col - 1, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row, col - 1, "w")
        self.set_letter(row, col + 1, "w")
        self.set_letter(row + 1, col + 1, "w")
        self.set_letter(row + 1, col - 1, "w")

    def circle_middle_of_boat_with_water(self, row, col):
        self.set_letter(row - 1, col - 1, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row + 1, col - 1, "w")
        self.set_letter(row + 1, col + 1, "w")

    def circle_bottom_of_boat_with_water(self, row, col):
        self.set_letter(row + 1, col, "w")
        self.set_letter(row + 1, col - 1, "w")
        self.set_letter(row + 1, col + 1, "w")
        self.set_letter(row, col - 1, "w")
        self.set_letter(row, col + 1, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row - 1, col - 1, "w")

    def circle_left_of_boat_with_water(self, row, col):
        self.set_letter(row - 1, col - 1, "w")
        self.set_letter(row - 1, col, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row, col - 1, "w")
        self.set_letter(row + 1, col - 1, "w")
        self.set_letter(row + 1, col, "w")
        self.set_letter(row + 1, col + 1, "w")

    def circle_right_of_boat_with_water(self, row, col):
        self.set_letter(row - 1, col - 1, "w")
        self.set_letter(row - 1, col, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row, col + 1, "w")
        self.set_letter(row + 1, col - 1, "w")
        self.set_letter(row + 1, col, "w")
        self.set_letter(row + 1, col + 1, "w")

    def circle_unknown_boat_with_water(self, row, col):
        self.set_letter(row - 1, col - 1, "w")
        self.set_letter(row - 1, col + 1, "w")
        self.set_letter(row + 1, col - 1, "w")
        self.set_letter(row + 1, col + 1, "w")

    @classmethod
    def from_board(cls, board):
        """ este metodo foi criada para testar a funcao count_boats e serve para se conseguir ler um
        input que contem uma board ja feita (como os .out do projeto). Deve possivelmente ser removido quando
        o projeto for concluido. """
        return cls(board, None, None, None, None, 10, 10, [], True)

    def copy(self):
        """Creates a copy of the Board."""
        new_board = np.copy(self.board)
        new_values_to_add_row_counts = self.values_to_add_row_counts.copy()
        new_values_to_add_col_counts = self.values_to_add_col_counts.copy()
        new_num_boats_to_add = self.num_boats_to_add
        new_free_row_counts = self.free_row_counts.copy()
        new_free_col_counts = self.free_col_counts
        return Board(new_board, new_values_to_add_row_counts, new_values_to_add_col_counts, new_free_row_counts,
                     new_free_col_counts,
                     self.LEN_ROW, self.LEN_COLUMN, new_num_boats_to_add, True)

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
        values_to_add_row_counts = [int(num) for num in sys.stdin.readline().split()[1:]]
        values_to_add_col_counts = [int(num) for num in sys.stdin.readline().split()[1:]]
        free_row_counts = [10 for i in range(10)]
        free_col_counts = [10 for i in range(10)]
        numOfHints = int(sys.stdin.readline())
        hints = []
        board = np.full((LEN_ROW, LEN_COLUMN), "*")

        for i in range(numOfHints):
            hint = sys.stdin.readline().split()[1:]
            hints.append(tuple(hint))

        for hint in hints:
            row, col, letter = hint
            board[int(row)][int(col)] = letter
            free_row_counts[int(row)] -= 1
            free_col_counts[int(col)] -= 1
            if letter != 'W':
                values_to_add_row_counts[int(row)] -= 1
                values_to_add_col_counts[int(col)] -= 1

        return Board(board, values_to_add_row_counts, values_to_add_col_counts, free_row_counts, free_col_counts,
                     LEN_ROW, LEN_COLUMN, [], False)

    # Important still doing it. Have to do what kind of ships can be added in each position
    def possible_actions(self):
        """Devolve uma lista com possiveis acoes i.e: posicoes livres
        onde eh possivel introduzir um barco"""
        possible_actions = []

        for row in range(self.LEN_ROW):
            for col in range(self.LEN_COLUMN):
                if self.get_letter(row, col) == "None":
                    possible_actions.append((row, col, "t"))
                    possible_actions.append((row, col, "b"))
                    possible_actions.append((row, col, "c"))
                    possible_actions.append((row, col, "m"))
        return possible_actions
    
    def is_board_fully_filled(self) -> bool:
        for i in self.values_to_add_row_counts:
            if i != 0:
                return False
        for i in self.values_to_add_col_counts:
            if i != 0:
                return False
        return True

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

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        print("ACTIONS:")
        print(state.board.biggest_boat_positions())
        print("BOARD:")
        state.board.print()
        return state.board.biggest_boat_positions()
    

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        print(state.state_id, action)
        new_board = state.board.copy()
        new_board.apply_action(action)
        print("NEW BOARD:")
        new_board.print()
        return BimaruState(new_board)

    def goal_test(self, state: BimaruState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.is_board_fully_filled() and state.board.num_boats_to_add == [0, 0, 0, 0]

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
    # TODO: outros metodos da classe


if __name__ == "__main__":
    # Ler grelha do ficheiro 'i1.txt' (Figura 1):
    # $ python3 bimaru.py < i1.txt
    board = Board.parse_instance()
    # Criar uma instância de Bimaru:
    board.print()
    print(board.biggest_boat_positions())