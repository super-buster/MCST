import numpy as np
from mcts.game.common import TwoPlayerGameState


class Gravity4bonuschessMove(object):
    def __init__(self, x_coordinate, y_coordinate, z_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.z_coordinate = z_coordinate
        self.value = value

    def __str__(self):
        return("x:{0} y:{1} z:{2} v:{3} \n".format(
            self.x_coordinate, self.y_coordinate, self.z_coordinate, self.value))


class Gravity4bonuschessGameState(TwoPlayerGameState):
    x = 1
    o = -1

    def __init__(self, state, move, next_to_move=1):
        if len(state.shape) != 3 or state.shape[0] != state.shape[1] or state.shape[0] != state.shape[2]:
            raise ValueError("Only 3D cube boards allowed")
        self.board = state
        self.nop = np.sum(np.absolute(self.board), 0).astype(int)
        self.board_size = state.shape[0]
        self.next_to_move = next_to_move
        if move is not None:
            self.move = move
            self.board[self.nop[move.x_coordinate][move.y_coordinate],
                       move.x_coordinate, move.y_coordinate] = move.value

    def whowin(self, *unknow):
        for item in unknow:
            if item == self.board_size:
                return self.x
            elif item == -self.board_size:
                return self.o
        return None

    @property
    def game_result(self):
        '''
        check if game is over
        '''
        vertical_sum = np.sum(
            self.board[..., self.move.x_coordinate, self.move.y_coordinate])
        row_sum = np.sum(
            self.board[self.move.z_coordinate][self.move.x_coordinate])
        col_sum = np.sum(
            self.board[self.move.z_coordinate][:, self.move.y_coordinate:self.move.y_coordinate+1])

        if self.whowin(vertical_sum, row_sum, col_sum) != None:
            return self.whowin(vertical_sum, row_sum, col_sum)

        # check the plane trace and diagonal
        # first judge which line
        if self.move.z_coordinate == self.board_size:
            trace1, trace2, trace3, trace4 = 0, 0, 0, 0
            if self.move.x_coordinate == 0:
                trace1 = self.board[3][0][self.move.y_coordinate] + \
                    self.board[2][1][self.move.y_coordinate] + \
                    self.board[1][2][self.move.y_coordinate] + \
                    self.board[0][3][self.move.y_coordinate]
                # 3,0,0
                if self.move.y_coordinate == 0:
                    diagonal = self.board[3][0][0] + \
                        self.board[2][1][1]+self.board[1][2][2] + \
                        self.board[0][3][3]
            if self.move.x_coordinate == 3:
                trace2 = self.board[0][0][self.move.y_coordinate] + \
                    self.board[1][1][self.move.y_coordinate] + \
                    self.board[2][2][self.move.y_coordinate] + \
                    self.board[3][3][self.move.y_coordinate]
                # 3, 3,3
                if self.move.y_coordinate == 3:
                    diagonal = self.board[3][3][3] + \
                        self.board[2][2][2]+self.board[1][1][1] + \
                        self.board[0][0][0]
            if self.move.y_coordinate == 0:
                trace3 = self.board[3][self.move.x_coordinate][0] +\
                    self.board[2][self.move.x_coordinate][1] + \
                    self.board[1][self.move.x_coordinate][2] + \
                    self.board[0][self.move.x_coordinate][3]
                # 3,3,0
                if self.move.y_coordinate == 0:
                    diagonal = self.board[3][3][0] + \
                        self.board[2][2][1]+self.board[1][1][2] + \
                        self.board[0][0][3]
            if self.move.y_coordinate == 3:
                trace4 = self.board[0][self.move.x_coordinate][0] +\
                    self.board[1][self.move.x_coordinate][1] + \
                    self.board[2][self.move.x_coordinate][2] + \
                    self.board[3][self.move.x_coordinate][3]
                # 3,0,3
                if self.move.x_coordinate == 0:
                    diagonal = self.board[3][0][3] + \
                        self.board[2][1][2]+self.board[1][2][1] + \
                        self.board[0][3][0]
            if self.whowin(trace1, trace2, trace3, trace4, diagonal) != None:
                return self.whowin(trace1, trace2, trace3, trace4)
        # tie
        if np.all(self.board != 0):
            return 0
        # if not over
        return None

    def is_game_over(self):
        return self.game_result is not None

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

        if move.z_coordinate >= 3:
            return False

        # finally check if board field not occupied yet
        return self.board[self.nop[move.x_coordinate, move.y_coordinate], move.x_coordinate, move.y_coordinate] == 0

    # move and change next_to_move
    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " +
                             self.board + " is not legal")
        next_to_move = Gravity4bonuschessGameState.o if self.next_to_move == Gravity4bonuschessGameState.x else Gravity4bonuschessGameState.x
        return Gravity4bonuschessGameState(self.board, move, next_to_move)

    def get_legal_actions(self):
        # return the row,column tuple where the value on the board is zero
        indices = np.where(self.nop < 3)
        return [Gravity4bonuschessMove(x, y, self.nop[x][y], self.next_to_move) for x, y in zip(indices[0], indices[1])]
