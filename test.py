import unittest
import numpy as np
from mcts.game.gravity4bonuschess import Gravity4bonuschessGameState, Gravity4bonuschessMove


class Gravity4bonuschessGameStateTestCase(unittest.TestCase):
    def setUp(self):
        self.state = np.zeros((4, 4, 4))
        self.move = None
        self.root = Gravity4bonuschessGameState(
            self.state, self.move, next_to_move=1)

    def test_whowin(self):
        print(self.root.whowin(1, 2, 4, -4))

    def test_get_legal_actions(self):
        actions = self.root.get_legal_actions()
        print(len(actions))

    def test_is_move_legal(self):
        state = np.zeros((4, 4, 4))
        state[0] = [[0, 1, -1, 1], [0, 1, -1, 0], [1, 0, 1, 1], [-1, -1, 0, 0]]
        move = Gravity4bonuschessMove(2, 1, 1)
        new_state = Gravity4bonuschessGameState(state, move, 1)

    def test_move(self):
        actions = self.root.get_legal_actions()
        new_state = self.root.move(actions[0])
        print(self.root.board)

    def test_game_result(self):
        b1 = [[1, 1, 1, -1], [-1, -1, 1, 1], [-1, 1, -1, 1], [1, -1, -1, -1]]
        b2 = [[0, 0, -1, -1], [-1, 0, -1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]]
        b3 = [[0, 0, -1, 1], [-1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
        b4 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        board = np.array((b1, b2, b3, b4))
        mv = Gravity4bonuschessMove(2, 1, 1)
        state = Gravity4bonuschessGameState(board, mv, next_to_move=1)
        assert state.game_result == state.x
        board2 = np.ones((4, 4, 4), dtype=int)
        state2 = Gravity4bonuschessGameState(board2, mv, next_to_move=-1)
        assert state2.get_legal_actions() is None
        state3 = Gravity4bonuschessGameState(
            np.zeros((4, 4, 4)), None, next_to_move=1)
        assert state3.is_move_legal(mv) == True


if __name__ == "__main__":
    unittest.main(verbosity=2)
