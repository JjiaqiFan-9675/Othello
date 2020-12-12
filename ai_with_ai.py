from othello_board import Board
import ai_method as AI

'''
    You could see how two AI friends compete with each other in this file!
'''
class AI_WITH_AI:
    def __init__(self, size, index):

        self.size = size
        self.index = index

        self.block = size

        self.AI_RANDOM = 1
        self.AI_MINIMAX = -1

        self.player = self.AI_RANDOM


        self.winner = 0
        self.NOT_FINISH = -1
        self.RANDOM_WIN = 1
        self.MINIMAX_WIN = 2

        self.random_actions = 0
        self.minimax_actions = 0

        self.result = []

        self.oth = Board(self.size, self.block)

        self.data = []

        self.game_begin()


    def random_minimax_turn(self, actions):
        if self.player == self.AI_RANDOM:
            action = AI.random_method(actions)
            self.oth.player_action(action)
            self.random_actions += len(actions)
        elif self.player == self.AI_MINIMAX:
            action = AI.minimax_method(actions, self.oth)
            self.oth.ai_action(action)
            self.minimax_actions += len(actions)

        self.oth.get_current_score()

        return self.oth.board.copy(), self.oth.player_node, self.oth.ai_node


    def game_begin(self):
        while True:
            actions = self.oth.action_valid(self.player)
            self.winner = self.oth.finish(actions)

            if self.winner == self.NOT_FINISH:
                board, player_score, ai_score = self.random_minimax_turn(actions)
                if self.player == self.AI_RANDOM:
                    score = player_score - ai_score
                else:
                    score = ai_score - player_score
                self.data.append((board, score))
                self.player *= -1
            else:
                self.result = [self.index, self.random_actions, self.minimax_actions, self.oth.player_node, self.oth.ai_node, self.winner]
                break

    def get_result(self):
        return self.result

