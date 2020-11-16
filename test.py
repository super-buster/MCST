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
        assert len(actions) == 16

    def test_is_move_legal(self):
        state = np.zeros((4, 4, 4))
        state[0] = [[0, 1, -1, 1], [0, 1, -1, 0], [1, 1, 1, 1], [-1, -1, 0, 0]]
        move = Gravity4bonuschessMove(2, 1, 0, 1)
        new_state = Gravity4bonuschessGameState(state, move, 1)
        assert new_state.game_result == 1
        assert new_state.is_game_over() is True

    def test_move(self):
        actions = self.root.get_legal_actions()[0]
        move = Gravity4bonuschessMove(
            actions.x_coordinate, actions.y_coordinate, actions.z_coordinate, 1)
        self.root.move(move)

    def test_game_result(self):
        actions = self.root.get_legal_actions()[0]
        move = Gravity4bonuschessMove(
            actions.x_coordinate, actions.y_coordinate, actions.z_coordinate, 1)
        new_state = self.root.move(move)
        assert new_state.game_result is None


if __name__ == "__main__":
    unittest.main(verbosity=2)
