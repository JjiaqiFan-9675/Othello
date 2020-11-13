import numpy as np
import random

'''
    This is the state of the game board!
'''

class Board:
    def __init__(self, size, block):
        self.size = size

        # static constant
        self.PLAYER_COLOR = 1
        self.AI_COLOR = -1
        self.WALL = 2
        self.EMPTY = 0

        # Each side has 2 pieces at start
        self.player_node = 2
        self.ai_node = 2

        # initialize board
        self.board = np.zeros((size, size), dtype=int)
        self.last_board_state = self.board.copy()

        # initialize four starting pieces
        self.board[int(size / 2)-1][int(size / 2)-1] = self.PLAYER_COLOR
        self.board[int(size / 2)-1][int(size / 2)] = self.AI_COLOR
        self.board[int(size / 2)][int(size / 2)-1] = self.AI_COLOR
        self.board[int(size / 2)][int(size / 2)] = self.PLAYER_COLOR
        self.block = block
        self.blocks = self.create_block()

    def create_block(self):
        blocks = []
        while len(blocks) < self.block:
            row = random.randint(0,self.size-1)
            col = random.randint(0,self.size-1)
            if self.board[row][col] == self.EMPTY:
                blocks.append([row, col])
                self.board[row][col] = self.WALL

        return blocks

    def get_current_score(self):
        ai_node = 0
        player_node = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.AI_COLOR:
                    ai_node += 1
                elif self.board[i][j] == self.PLAYER_COLOR:
                    player_node += 1
        self.ai_node = ai_node
        self.player_node = player_node

    def action_valid(self, player):
        actions = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player * -1:
                    # up
                    row = i
                    while row > 0 and self.board[row][j] == player * -1: row -= 1
                    if row >= 0 and i < self.size - 1 and self.board[row][j] == player and self.board[i + 1][j] == 0:
                        actions.add((i + 1, j))

                    # down
                    row = i
                    while row < self.size - 1 and self.board[row][j] == player * -1: row += 1
                    if i > 0 and row <= self.size - 1 and self.board[row][j] == player and self.board[i - 1][j] == 0:
                        actions.add((i - 1, j))

                    # left
                    col = j
                    while col > 0 and self.board[i][col] == player * -1: col -= 1
                    if col >= 0 and j < self.size - 1 and self.board[i][col] == player and self.board[i][j + 1] == 0:
                        actions.add((i, j + 1))

                    # right
                    col = j
                    while col < self.size - 1 and self.board[i][col] == player * -1: col += 1
                    if j > 0 and col <= self.size - 1 and self.board[i][col] == player and self.board[i][j - 1] == 0:
                        actions.add((i, j - 1))

                    # upper left
                    row, col = i, j
                    while row > 0 and col > 0 and self.board[row][col] == player * -1:
                        row -= 1
                        col -= 1
                    if row >= 0 and col >= 0 \
                            and i < self.size - 1 and j < self.size - 1 \
                            and self.board[row][col] == player and self.board[i + 1][j + 1] == 0:
                        actions.add((i + 1, j + 1))

                    # upper right
                    row, col = i, j
                    while row > 0 and col < self.size and self.board[row][col] == player * -1:
                        row -= 1
                        col += 1
                    if row >= 0 and col <= self.size - 1 \
                            and i < self.size - 1 and j > 0 \
                            and self.board[row][col] == player and self.board[i + 1][j - 1] == 0:
                        actions.add((i + 1, j - 1))

                    # lower left
                    row, col = i, j
                    while row < self.size - 1 and col > 0 and self.board[row][col] == player * -1:
                        row += 1
                        col -= 1
                    if row <= self.size - 1 and col >= 0 \
                            and i > 0 and j < self.size - 1 \
                            and self.board[row][col] == player and self.board[i - 1][j + 1] == 0:
                        actions.add((i - 1, j + 1))

                    # lower right
                    row, col = i, j
                    while row < self.size - 1 and col < self.size - 1 and self.board[row][col] == player * -1:
                        row += 1
                        col += 1
                    if row <= self.size - 1 and col <= self.size - 1 \
                            and i > 0 and j > 0 \
                            and self.board[row][col] == player and self.board[i - 1][j - 1] == 0:
                        actions.add((i - 1, j - 1))

        return list(actions)

    # Player is 1
    def player_action(self, action):
        self.last_board_state = self.board.copy()

        self.change(action, self.PLAYER_COLOR)
        self.board[action[0]][action[1]] = self.PLAYER_COLOR

    # AI is -1
    def ai_action(self, action):
        self.last_board_state = self.board.copy()

        self.change(action, self.AI_COLOR)
        self.board[action[0]][action[1]] = self.AI_COLOR

    def backward(self):
        self.board = self.last_board_state.copy()

    def print_board(self):
        print(self.board)

    # if player win, return 1;
    # if computer win, return 2;
    # if both win, return 0;
    # if game not finished, return -1;
    def finish(self, actions):
        if len(actions) == 0:
            self.get_current_score()
            if self.player_node > self.ai_node:
                return 1
            elif self.player_node < self.ai_node:
                return 2
            else:
                return 0

        return -1

    def change(self, action, player):
        row = action[0]
        col = action[1]

        up, down, left, right = row, row, col, col

        if row > 0: up = row - 1
        if row < self.size - 1: down = row + 1
        if col > 0: left = col - 1
        if col < self.size - 1: right = col + 1

        # check up
        while up > 0 and self.board[up][col] == player * -1:
            up -= 1
        if self.board[up][col] == player:
            if row > 0: up = row - 1
            while up > 0 and self.board[up][col] == player * -1:
                self.board[up][col] = player
                up -= 1

        # check down
        while down < self.size - 1 and self.board[down][col] == player * -1:
            down += 1
        if self.board[down][col] == player:
            if row < self.size - 1: down = row + 1
            while down < self.size - 1 and self.board[down][col] == player * -1:
                self.board[down][col] = player
                down += 1

        # check left
        while left > 0 and self.board[row][left] == player * -1:
            left -= 1
        if self.board[row][left] == player:
            if col > 0: left = col - 1
            while left > 0 and self.board[row][left] == player * -1:
                self.board[row][left] = player
                left -= 1

        # check right
        while right < self.size - 1 and self.board[row][right] == player * -1:
            right += 1
        if self.board[row][right] == player:
            if col < self.size - 1: right = col + 1
            while right < self.size - 1 and self.board[row][right] == player * -1:
                self.board[row][right] = player
                right += 1

        # check upper left
        if row > 0: up = row - 1
        if col > 0: left = col - 1
        while up > 0 and left > 0 and self.board[up][left] == player * -1:
            up -= 1
            left -= 1
        if self.board[up][left] == player:
            if row > 0: up = row - 1
            if col > 0: left = col - 1
            while up > 0 and left > 0 and self.board[up][left] == player * -1:
                self.board[up][left] = player
                up -= 1
                left -= 1

        # check upper right
        if row > 0: up = row - 1
        if col < self.size - 1: right = col + 1
        while up > 0 and right < self.size - 1 and self.board[up][right] == player * -1:
            up -= 1
            right += 1
        if self.board[up][right] == player:
            if row > 0: up = row - 1
            if col < self.size - 1: right = col + 1
            while up > 0 and right < self.size - 1 and self.board[up][right] == player * -1:
                self.board[up][right] = player
                up -= 1
                right += 1

        # check down left
        if row < self.size - 1: down = row + 1
        if col > 0: left = col - 1
        while down < self.size - 1 and left > 0 and self.board[down][left] == player * -1:
            down += 1
            left -= 1
        if self.board[down][left] == player:
            if row < self.size - 1: down = row + 1
            if col > 0: left = col - 1
            while down < self.size - 1 and left > 0 and self.board[down][left] == player * -1:
                self.board[down][left] = player
                down += 1
                left -= 1

        # check down right
        if row < self.size - 1: down = row + 1
        if col < self.size - 1: right = col + 1
        while down < self.size - 1 and right < self.size - 1 and self.board[down][right] == player * -1:
            down += 1
            right += 1
        if self.board[down][right] == player:
            if row < self.size - 1: down = row + 1
            if col < self.size - 1: right = col + 1
            while down < self.size - 1 and right < self.size - 1 and self.board[down][right] == player * -1:
                self.board[down][right] = player
                down += 1
                right += 1





