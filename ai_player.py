import random
from othello_board import Board

class AI:

    def random_method(actions):
        action = actions[random.randint(0, len(actions) - 1)]
        return action

    # 4 depth
    def minimax_method(othello, actions, player, depth):
        score = -1000

        for action in actions:
            othello.ai_action(action)

            new_actions = othello.action_valid(player*-1)
            new_score, _ = AI.minimax_method(othello, new_actions, player*-1, depth-1)
            if new_score > score:
                act = action
            othello.backward()

        return score, act

