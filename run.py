import numpy as np
from mcts.tree.nodes import *
from mcts.tree.search import *
from mcts.game.tictactoe import TicTacToeGameState, TicTacToeMove
from mcts.game.pui import conf, puiinit, screen, Draw
import pygame
import sys


def AiFirst():
    state = np.zeros((3, 3))
    initial_board_state = TicTacToeGameState(
        state=state, next_to_move=1)
    root = TwoPlayersGameMonteCarloTreeSearchNode(
        state=initial_board_state, parent=None)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(1000)
    coordinate = np.where((state == 0) & (best_node.state.board == 1))
    # print(coordinate[0][0], coordinate[1][0])
    c_state = best_node.state
    return c_state, coordinate


def PlayerFirst():
    state = np.zeros((3, 3))
    initial_board_state = TicTacToeGameState(
        state=state, next_to_move=-1)
    return initial_board_state


def get_action(state, x, y):
    try:
        move = TicTacToeMove(x, y, -1)
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
        pygame.quit()
        sys.exit()
        return 1
    else:
        return -1


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    puiinit()
    # c_state, coordinate = AiFirst()
    # Draw(coordinate[0][0], coordinate[1][0], "o")
    c_state = PlayerFirst()
    # main loop
    while True:
        pygame.display.update()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()
            if c_state.next_to_move == 1:
                board_state = TicTacToeGameState(
                    state=c_board, next_to_move=1)
                root = TwoPlayersGameMonteCarloTreeSearchNode(
                    state=board_state, parent=None)
                # we build a new tree, but actually we can reuse the search infomation before
                mcts = MonteCarloTreeSearch(root)
                best_node = mcts.best_action(1000)
                coordinate = np.where(
                    (c_board == 0) & (best_node.state.board == 1))
                Draw(coordinate[0][0], coordinate[1][0], "o")
                c_state = best_node.state
                if judge(c_state) == 1:
                    break
                elif judge(c_state) == -1:
                    continue
            if event.type == pygame.MOUSEBUTTONDOWN and c_state.next_to_move == -1:
                corx, cory = pygame.mouse.get_pos()
                corx, cory = 3*corx//conf.WIDTH, 3*cory//conf.HEIGHT
                move1 = get_action(c_state, corx, cory)
                c_state = c_state.move(move1)
                c_board = c_state.board
                Draw(corx, cory, "x")
                if judge(c_state) == 1:
                    break
                elif judge(c_state) == -1:
                    continue
