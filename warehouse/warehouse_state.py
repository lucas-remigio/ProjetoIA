import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray

import constants
from agentsearch.state import State
from agentsearch.action import Action
from warehouse.actions import *


class WarehouseState(State[Action]):

    def __init__(self, matrix: ndarray, rows, columns):
        super().__init__()
        # TODO

        self.products = 0
        self.rows = rows
        self.columns = columns
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)

        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == constants.FORKLIFT:
                    self.line_forklift = i
                    self.column_forklift = j
                if self.matrix[i][j] == constants.EXIT:
                    self.line_exit = i
                    self.column_exit = j
                if self.matrix[i][j] == constants.PRODUCT:
                    self.products += 1

    '''
    nos can_moves horizontais o agente apenas pode andar para o lado se não estiver numa das bordas
    horizontais e quiser-se mover para OutOfBounds e se não for um prateleira. Pode mover se ao lado for uma
    célula vazia ou um produto
    
    nos can_moves verticais o agente apenas pode andar para cima ou baixo se não estiver numa das bordas
    verticais e quiser-se mover para OutOfBounds e se não for um prateleira ou um produto. Pode mover se ao 
    lado for uma célula vazia
    '''

    def can_move_up(self) -> bool:

        if self.line_forklift > 0:
            forklift_up = self.matrix[self.line_forklift - 1][self.column_forklift]
            if forklift_up != constants.SHELF and forklift_up != constants.PRODUCT:
                return True
        return False

    def can_move_right(self) -> bool:

        if self.column_forklift < self.columns - 1:
            forklift_right = self.matrix[self.line_forklift][self.column_forklift + 1]
            if forklift_right != constants.SHELF and forklift_right != constants.PRODUCT:
                return True
        return False

    def can_move_down(self) -> bool:

        if self.line_forklift < self.rows - 1:
            forklift_down = self.matrix[self.line_forklift + 1][self.column_forklift]
            if forklift_down != constants.SHELF and forklift_down != constants.PRODUCT:
                return True
        return False

    def can_move_left(self) -> bool:

        if self.column_forklift > 0:
            forklift_left = self.matrix[self.line_forklift][self.column_forklift - 1]
            if forklift_left != constants.SHELF and forklift_left != constants.PRODUCT:
                return True
        return False

    def move_up(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.matrix[self.line_forklift - 1][self.column_forklift] = constants.FORKLIFT
        self.line_forklift -= 1

    def move_right(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.matrix[self.line_forklift][self.column_forklift + 1] = constants.FORKLIFT
        self.column_forklift += 1

    def move_down(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.matrix[self.line_forklift + 1][self.column_forklift] = constants.FORKLIFT
        self.line_forklift += 1

    def move_left(self) -> None:
        self.matrix[self.line_forklift][self.column_forklift] = constants.EMPTY
        self.matrix[self.line_forklift][self.column_forklift - 1] = constants.FORKLIFT
        self.column_forklift -= 1

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.line_forklift or column != self.column_forklift):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    def __hash__(self):
        return hash(self.matrix.tostring())
