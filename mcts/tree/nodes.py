import numpy as np
import math
from collections import defaultdict


class MonteCarloTreeSearchNode(object):

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

    @property
    def untried_actions(self):
        pass

    # q.setter q means Total simulation reward
    @property
    def q(self):
        pass

    # n means Total number of visits
    @property
    def n(self):
        pass

    def expand(self):
        pass

    # simulation
    def rollout(self):
        pass

    # backpropagate from node which starts simulation to root
    def backpropagate(self, reward):
        pass

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    # the core of MCTS
    # compute UTC
    def best_child(self, c_param=0.7):
        choices_weights = [
            (c.q/c.n) + c_param * np.sqrt((2*np.log(self.n)/c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        try:
            return possible_moves[np.random.randint(len(possible_moves))]
        except ValueError as e:
            print(len(possible_moves))


class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):
    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        self._number_of_visits = 0.
        # return 0 if key not exists
        self._results = defaultdict(int)
        self._untried_actions = None

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = self.state.get_legal_actions()
        return self._untried_actions

    @property
    def q(self):
        # for player1 , q equals results[1]-results[-1]; else results[-1]-results[1]
        wins = self._results[self.parent.state.next_to_move]
        loses = self._results[-1 * self.parent.state.next_to_move]
        return wins - loses

    @property
    def n(self):
        return self._number_of_visits

    # take a step from selected node
    def expand(self):
        # remove the last value to ensure we take a different action
        action = self.untried_actions.pop()
        next_state = self.state.move(action)    
        child_node = TwoPlayersGameMonteCarloTreeSearchNode(
            next_state, parent=self
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    # play out game till ends
    def rollout(self):
        current_rollout_state = self.state
        while not current_rollout_state.is_game_over():
            possible_moves = current_rollout_state.get_legal_actions()
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.move(action)
        return current_rollout_state.game_result

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)
