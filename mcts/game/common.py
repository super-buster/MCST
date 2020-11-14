class TwoPlayerGameState(object):
    def game_result(self):
        '''
        1 if player1 wins
        -1 if player2 wins
        0 if there is a tie
        '''
        pass

    def is_game_over(self):
        pass

    def move(self,action):
        pass

    def get_legal_actions(self):
        '''
        return list of legal action at current game state
        '''
        pass
