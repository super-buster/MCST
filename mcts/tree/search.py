######################################################################
# ref1: https://zhuanlan.zhihu.com/p/30458774                        #
# ref2: https://github.com/int8/monte-carlo-tree-search/tree/master/ #
# ref3: https://zhuanlan.zhihu.com/p/59567014                        #
######################################################################

class MonteCarloTreeSearch(object):
    '''
    node : mctspy.tree.nodes.MonteCarloTreeSearchNode
    '''
    def __init__(self,node) :
        self.root=node

    def best_action(self,simulations_number):
        # first we palyout all the subnode of root
        for _ in range(0,simulations_number):
            v=self._tree_policy()
            reward=v.rollout()
            v.backpropagate(reward)
        #it is prediction, so just to select best child go for exploitation only
        return self.root.best_child(c_param=0)

    # implement selection and expansion
    def _tree_policy(self):
        '''
        selects node to rollout
        '''
        current_node=self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node=current_node.best_child()
        return current_node
