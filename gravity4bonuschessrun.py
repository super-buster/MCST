import numpy as np
from mcts.tree.nodes import *
from mcts.tree.search import *
from mcts.game.gravity4bonuschess import Gravity4bonuschessGameState, Gravity4bonuschessMove
import sys


def Aifirst():
    state = np.zeros((4, 4, 4))
    move = None
    initial_board_state = Gravity4bonuschessGameState(
        state, move, next_to_move=1)
    root = TwoPlayersGameMonteCarloTreeSearchNode(
        state=initial_board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(1500)
    c_state = best_node.state
    return c_state


def get_action(state, x, y, z):
    try:
        move = Gravity4bonuschessMove(x, y, -1)
    except Exception as e:
        move = -1
    if move == -1 or not state.is_move_legal(move):
        print("invalid move")
    return move


def judge(state):
    if state.is_game_over():
        if state.game_result == 1.0:
            print("You lose!")
        if state.game_result == 0.0:
            print("Tie!")
        if state.game_result == -1.0:
            print("You Win!")
        return 1
    else:
        return -1


if __name__ == "__main__":
    c_state = Aifirst()
    while True:
        print("input you move: x,y")
        x, y = input()
        print(c_state.board)
