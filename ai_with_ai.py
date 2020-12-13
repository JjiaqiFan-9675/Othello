from othello_board import Board
import ai_method as AI
import copy

'''
    You could see how two AI friends compete with each other in this file!
    This includes:
        Random AI with Minimax Tree AI:  def random_minimax_game_begin()
        Minimax Tree AI with Minimax Tree AI:  def minimax_minimax_game_begin()
        Minimax Tree AI with CNN AI:  def minimax_cnn_game_begin(self)
'''
class AI_WITH_AI:
    def __init__(self, size, index, net):

        self.size = size
        self.index = index
        self.net = net

        self.block = size

        self.PLAYER = 1
        self.AI = -1

        self.player = self.PLAYER

        self.winner = 0
        self.NOT_FINISH = -1
        self.RANDOM_WIN = 1
        self.MINIMAX_WIN = 2

        self.random_actions = 0
        self.minimax_actions = 0
        self.cnn_actions = 0

        self.result = []

        self.oth = Board(self.size, self.block)

        self.data = []


    def random_minimax_turn(self, actions):
        if self.player == self.PLAYER:
            action = AI.random_method(actions)
            self.oth.player_action(action)
            self.random_actions += len(actions)
        elif self.player == self.AI:
            action = AI.minimax_method(actions, self.oth)
            self.oth.ai_action(action)
            self.minimax_actions += len(actions)


    def minimax_minimax_turn(self, actions):
        if self.player == self.PLAYER:
            action = AI.minimax_player_method(actions, self.oth)
            self.oth.player_action(action)
        elif self.player == self.AI:
            action = AI.minimax_method(actions, self.oth)
            self.oth.ai_action(action)

        self.oth.get_current_score()

        return copy.deepcopy(self.oth)

    def minimax_cnn_turn(self, actions):
        if self.player == self.PLAYER:
            action = AI.minimax_method(actions, self.oth)
            self.oth.player_action(action)
            self.minimax_actions += len(actions)
        else:
            action = AI.cnn_method(self.net, actions, self.oth)
            self.oth.ai_action(action)
            self.cnn_actions += len(actions)


    def random_minimax_game_begin(self):
        while True:
            actions = self.oth.action_valid(self.player)
            self.winner = self.oth.finish(actions)

            if self.winner == self.NOT_FINISH:
                self.random_minimax_turn(actions)
                self.player *= -1
            else:
                self.result = [self.index, self.random_actions, self.minimax_actions, self.oth.player_node, self.oth.ai_node, self.winner, self.score]
                break

    def minimax_minimax_game_begin(self):
        while True:
            actions = self.oth.action_valid(self.player)
            self.winner = self.oth.finish(actions)

            if self.winner == self.NOT_FINISH:
                state = self.minimax_minimax_turn(actions)
                self.player *= -1
                for action in state.action_valid(self.player):
                    if self.player == self.PLAYER:
                        state.player_action(action)
                    else:
                        state.ai_action(action)

                    state.get_current_score()
                    self.data.append((state.board, state.ai_node - state.player_node))
                    state.backward()
            else:
                break

    def minimax_cnn_game_begin(self):
        while True:
            actions = self.oth.action_valid(self.player)
            self.winner = self.oth.finish(actions)

            if self.winner == self.NOT_FINISH:
                self.minimax_cnn_turn(actions)
                self.player *= -1
            else:
                self.oth.get_current_score()
                self.result = [self.index, self.random_actions, self.minimax_actions, self.oth.player_node, self.oth.ai_node, self.winner, self.oth.ai_node-self.oth.player_node]
                break

    def get_result(self):
        return self.result

    def get_data(self):
        return self.data