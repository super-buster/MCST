######################################################################
# ref1: https://zhuanlan.zhihu.com/p/30458774                        #
# ref2: https://github.com/int8/monte-carlo-tree-search/tree/master/ #
# ref3: https://zhuanlan.zhihu.com/p/59567014                        #
######################################################################
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
    best_node = mcts.best_action(2000)
    c_state = best_node.state
    return c_state


def get_action(state):
    try:
        location = input("Your move(x,y): ")
        if isinstance(location, str):
            location = [int(n, 10) for n in location.split(",")]
        if len(location) != 2:
            move = -1
        x = location[0]
        y = location[1]
        move = Gravity4bonuschessMove(x, y, -1)
    except Exception as e:
        move = -1
    if move == -1 or not state.is_move_legal(move):
        print("invalid move")
        move = get_action(state)
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
    print(c_state.board)
    while True:
        move1 = get_action(c_state)
        c_state = c_state.move(move1)
        if judge(c_state) == 1:
            break
        root = TwoPlayersGameMonteCarloTreeSearchNode(
            state=c_state, parent=None)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.best_action(1500)
        c_state = best_node.state
        print("rival's move: ", c_state.source)
        print(c_state.board)
        if judge(c_state) == 1:
            break
        elif judge(c_state) == -1:
            continue
