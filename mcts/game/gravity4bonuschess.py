######################################################################
# ref1: https://zhuanlan.zhihu.com/p/30458774                        #
# ref2: https://github.com/int8/monte-carlo-tree-search/tree/master/ #
# ref3: https://zhuanlan.zhihu.com/p/59567014                        #
######################################################################
import numpy as np
import copy
from mcts.game.common import TwoPlayerGameState


class Gravity4bonuschessMove(object):
    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = 0
        self.value = value

    def __str__(self):
        return("x:{0} y:{1} z:{2} v:{3} \n".format(
            self.x_coordinate, self.y_coordinate, self.z_coordinate, self.value))

    def __repr__(self):
        return("x:{0} y:{1} z:{2} v:{3} \n".format(
            self.x_coordinate, self.y_coordinate, self.z_coordinate, self.value))


class Gravity4bonuschessGameState(TwoPlayerGameState):
    x = 1
    o = -1

    def __init__(self, state, move, next_to_move=1):
        if len(state.shape) != 3 or state.shape[0] != state.shape[1] or state.shape[0] != state.shape[2]:
            raise ValueError("Only 3D cube boards allowed")
        self.board = state
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move
        self.source = move
        self.nop = np.sum(np.absolute(self.board), 0).astype(int)

    def whowin(self, *unknow):
        for item in unknow:
            if item == self.board_size:
                return self.x
            elif item == -self.board_size:
                return self.o
        return None

    @ property
    def game_result(self):
        '''
        check if game is over
        '''
        # root
        if self.source is None:
            return None
        vertical_sum = np.sum(
            self.board[..., self.source.x_coordinate, self.source.y_coordinate])
        row_sum = np.sum(
            self.board[self.source.z_coordinate][self.source.x_coordinate])
        col_sum = np.sum(
            self.board[self.source.z_coordinate][:, self.source.y_coordinate:self.source.y_coordinate+1])
        diag_sum_tl = (self.board[self.source.z_coordinate]).trace()
        diag_sum_tr = (self.board[self.source.z_coordinate][::-1]).trace()
        result = self.whowin(vertical_sum, row_sum,
                             col_sum, diag_sum_tl, diag_sum_tr)
        if result != None:
            return result

        # check the plane trace and diagonal
        # first judge which line
        if self.source.z_coordinate == self.board_size:
            trace1, trace2, trace3, trace4 = 0, 0, 0, 0
            if self.source.x_coordinate == 0:
                trace1 = self.board[3][0][self.source.y_coordinate] + \
                    self.board[2][1][self.source.y_coordinate] + \
                    self.board[1][2][self.source.y_coordinate] + \
                    self.board[0][3][self.source.y_coordinate]
                # 3,0,0
                if self.source.y_coordinate == 0:
                    diagonal = self.board[3][0][0] + \
                        self.board[2][1][1]+self.board[1][2][2] + \
                        self.board[0][3][3]
            if self.source.x_coordinate == 3:
                trace2 = self.board[0][0][self.source.y_coordinate] + \
                    self.board[1][1][self.source.y_coordinate] + \
                    self.board[2][2][self.source.y_coordinate] + \
                    self.board[3][3][self.source.y_coordinate]
                # 3, 3,3
                if self.source.y_coordinate == 3:
                    diagonal = self.board[3][3][3] + \
                        self.board[2][2][2]+self.board[1][1][1] + \
                        self.board[0][0][0]
            if self.source.y_coordinate == 0:
                trace3 = self.board[3][self.source.x_coordinate][0] +\
                    self.board[2][self.source.x_coordinate][1] + \
                    self.board[1][self.source.x_coordinate][2] + \
                    self.board[0][self.source.x_coordinate][3]
                # 3,3,0
                if self.source.y_coordinate == 0:
                    diagonal = self.board[3][3][0] + \
                        self.board[2][2][1]+self.board[1][1][2] + \
                        self.board[0][0][3]
            if self.source.y_coordinate == 3:
                trace4 = self.board[0][self.source.x_coordinate][0] +\
                    self.board[1][self.source.x_coordinate][1] + \
                    self.board[2][self.source.x_coordinate][2] + \
                    self.board[3][self.source.x_coordinate][3]
                # 3,0,3
                if self.source.x_coordinate == 0:
                    diagonal = self.board[3][0][3] + \
                        self.board[2][1][2]+self.board[1][2][1] + \
                        self.board[0][3][0]
            if self.whowin(trace1, trace2, trace3, trace4, diagonal) != None:
                return self.whowin(trace1, trace2, trace3, trace4)
        # draw
        if np.all(self.board != 0):
            return 0
        # if not over
        return None

    def is_game_over(self):
        result = self.game_result
        return result is not None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board
        x_in_range = move.x_coordinate < self.board_size and move.x_coordinate >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = move.y_coordinate < self.board_size and move.y_coordinate >= 0
        if not y_in_range:
            return False

        if self.nop[move.x_coordinate][move.y_coordinate] > 3:
            return False

        # finally check if board field not occupied yet
        return self.board[self.nop[move.x_coordinate, move.y_coordinate]][move.x_coordinate][move.y_coordinate] == 0

    # move and change next_to_move
    def move(self, source):
        if not self.is_move_legal(source):
            print(self.nop, source)
            raise ValueError("move is not legal")
        next_to_move = Gravity4bonuschessGameState.o if self.next_to_move == Gravity4bonuschessGameState.x else Gravity4bonuschessGameState.x
        # must copy a new object,otherwise refer to the same object and cause root board be changed
        new_board = np.copy(self.board)
        new_source = copy.copy(source)
        new_source.z_coordinate = self.nop[source.x_coordinate][source.y_coordinate]
        new_board[new_source.z_coordinate][new_source.x_coordinate][new_source.y_coordinate] = new_source.value
        return Gravity4bonuschessGameState(new_board, new_source, next_to_move)

    def get_legal_actions(self):
        # return the row,column tuple if satisfy the condition
        indices = np.where(self.nop < self.board_size)
        if len(indices[0]) == 0:
            return None
        else:
            return [Gravity4bonuschessMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]
