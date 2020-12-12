import random
from othello_board import Board
import copy
import numpy as np
import torch as tr


'''
    This is the mode of your AI friends.
'''

def random_method(actions):
    action = actions[random.randint(0, len(actions) - 1)]
    return action

def minimax_method(actions, state):

    new_scores = []

    for action in actions:

        new_state = copy.deepcopy(state)
        new_state.ai_action(action)
        player_actions = new_state.action_valid(new_state.PLAYER_COLOR)

        # Minimax - AI assumes people to choose which benefit them most
        if len(player_actions) > 0:
            new_new_scores = []
            for player_action in player_actions:
                new_state.player_action(player_action)

                new_state.get_current_score()
                new_new_scores.append(new_state.ai_node - new_state.player_node)
                new_state.backward()

            new_state.player_action(player_actions[np.argmin(new_new_scores)])

        new_state.get_current_score()
        new_scores.append(new_state.ai_node - new_state.player_node)
        new_state.backward()

    # print(new_scores)
    decision = actions[np.argmax(new_scores)]
    return decision

def expectimax_method(actions, state):
    new_scores = []

    for action in actions:

        new_state = copy.deepcopy(state)
        new_state.ai_action(action)
        player_actions = new_state.action_valid(new_state.PLAYER_COLOR)

        # Expectimax - AI assumes people to choose randomly
        if len(player_actions) > 0:
            expect_score = 0
            for player_action in player_actions:
                possibility = 1. / (len(player_actions))

                new_state.player_action(player_action)
                expect_score += possibility * new_state.get_current_score()

                new_state.backward()

            new_scores.append(expect_score)

        else:
            new_scores.append(0)
        new_state.backward()

    decision = actions[np.argmax(new_scores)]
    return decision

def encode(board):
    row, col = board.shape
    onehot = tr.zeros(3, row, col)
    for r in range(row):
        for c in range(col):
            if board[r][c] == 2:
                onehot[0, r, c] = 0
            elif board[r][c] == 0:
                onehot[0, r, c] = 1
            elif board[r][c] == 1:
                onehot[1, r, c] = 1
            else:
                onehot[2, r, c] = 1
    return onehot

def cnn_method(net, actions, state):
    children = []
    for action in actions:
        new_state = copy.deepcopy(state)
        new_state.ai_action(action)
        children.append(encode(new_state.board))
        new_state.backward()

    with tr.no_grad():
        x = tr.stack(tuple(children))
        y = net(x)
        probs = tr.softmax(y.flatten(), dim=0)
        a = np.random.choice(len(probs), p=probs.detach().numpy())

    return actions[a]

