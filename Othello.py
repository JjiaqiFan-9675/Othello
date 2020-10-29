import numpy as np
import random

class Othello:
    def __init__(self, size, block):
        self.size = size

        # Each side has 2 pieces at start
        self.player = 2
        self.computer = 2

        # initialize board
        self.board = np.zeros((size, size), dtype=int)

        # initialize four starting pieces
        self.board[int(size / 2)-1][int(size / 2)-1] = -1
        self.board[int(size / 2)-1][int(size / 2)] = 1
        self.board[int(size / 2)][int(size / 2)-1] = 1
        self.board[int(size / 2)][int(size / 2)] = -1
        self.block = block
        self.blocks = self.create_block()

    def create_block(self):
        blocks = []
        while len(blocks) < self.block:
            row = random.randint(0,self.size-1)
            col = random.randint(0,self.size-1)
            if self.board[row][col] == 0:
                blocks.append([row, col])
                self.board[row][col] = 2

        return blocks

    def action_valid(self, play):
        actions = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == play * -1:
                    # up
                    row = i
                    while row > 0 and self.board[row][j] == play*-1: row -= 1
                    if row >= 0 and i < self.size -1 and self.board[row][j] == play and self.board[i+1][j] == 0:
                        actions.add((i+1,j))

                    # down
                    row = i
                    while row < self.size - 1 and self.board[row][j] == play*-1: row += 1
                    if i > 0 and row <= self.size - 1 and self.board[row][j] == play and self.board[i-1][j] == 0:
                        actions.add((i-1,j))

                    # left
                    col = j
                    while col > 0 and self.board[i][col] == play*-1: col -= 1
                    if col >= 0 and j < self.size -1 and self.board[i][col] == play and self.board[i][j+1] == 0:
                        actions.add((i,j+1))

                    # right
                    col = j
                    while col < self.size - 1 and self.board[i][col] == play * -1: col += 1
                    if j > 0 and col <= self.size - 1 and self.board[i][col] == play and self.board[i][j-1] == 0:
                        actions.add((i,j-1))

                    # upper left
                    row, col = i, j
                    while row > 0 and col > 0 and self.board[row][col] == play*-1: 
                        row -= 1
                        col -= 1
                    if row >= 0 and col >= 0\
                        and i < self.size - 1 and j < self.size - 1\
                        and self.board[row][col] == play and self.board[i+1][j+1] == 0:
                        actions.add((i+1, j+1))

                    # upper right
                    row, col = i, j
                    while row > 0 and col < self.size and self.board[row][col] == play*-1:
                        row -= 1
                        col += 1
                    if row >= 0 and col <= self.size - 1\
                        and i < self.size - 1 and j > 0\
                        and self.board[row][col] == play and self.board[i+1][j-1] == 0:
                        actions.add((i+1, j-1))

                    # lower left
                    row, col = i, j
                    while row < self.size - 1 and col > 0 and self.board[row][col] == play*-1:
                        row += 1
                        col -= 1
                    if row <= self.size - 1 and col >= 0\
                        and i > 0 and j < self.size - 1\
                        and self.board[row][col] == play and self.board[i-1][j+1] == 0:
                        actions.add((i-1, j+1))

                    # lower right
                    row, col = i, j
                    while row < self.size - 1 and col < self.size - 1 and self.board[row][col] == play*-1:
                        row += 1
                        col += 1
                    if row <= self.size - 1 and col <= self.size - 1 \
                        and i > 0 and j > 0 \
                        and self.board[row][col] == play and self.board[i-1][j-1] == 0:
                        actions.add((i-1, j-1))

        return list(actions)

    # player is 1
    def player_action(self, action):
        self.board[action[0]][action[1]] = 1
        self.player += 1

    # computer is -1
    def computer_action(self, actions):
        action = actions[random.randint(0,len(actions)-1)]
        print ("The AI chooses " + str(action))
        self.board[action[0]][action[1]] = -1
        self.computer += 1
        self.change(action, -1)

    def print_board(self):
        print(self.board)

    # if player win, return 1;
    # if computer win, return 2;
    # if both win, return 0;
    # if game not finished, return -1;
    def finish(self, actions):
        if self.block + self.player + self.computer == self.size * self.size or len(actions) == 0:
            if self.player > self.computer : return 1
            elif self.player < self.computer: return 2
            else: return 0

        return -1

    def change(self, action, play):
        row = action[0]
        col = action[1]

        # check if this player was surrounded by other player
        up, down, left, right = row, row, col, col

        if row > 0: up = row - 1
        if row < self.size - 1: down = row + 1
        if col > 0: left = col - 1
        if col < self.size - 1: right = col + 1 

        # check up
        while up > 0 and self.board[up][col] == play*-1:
            up -= 1 
        if self.board[up][col] == play:
            if row > 0: up = row - 1
            while up > 0 and self.board[up][col] == play*-1:
                self.board[up][col] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                up -= 1
        
        # check down
        while down < self.size - 1 and self.board[down][col] == play*-1:
            down += 1 
        if self.board[down][col] == play:
            if row < self.size - 1: down = row + 1
            while down < self.size - 1 and self.board[down][col] == play*-1:
                self.board[down][col] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                down += 1
        
        # check left
        while left > 0 and self.board[row][left] == play*-1:
            left -= 1
        if self.board[row][left] == play:
            if col > 0: left = col - 1
            while left > 0 and self.board[row][left] == play*-1:
                self.board[row][left] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                left -= 1
        
        # check right
        while right < self.size - 1 and self.board[row][right] == play*-1:
            right += 1
        if self.board[row][right] == play:
            if col < self.size - 1: right = col + 1 
            while right < self.size - 1 and self.board[row][right] == play*-1:
                self.board[row][right] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                right += 1

        # check upper left
        if row > 0: up = row - 1
        if col > 0: left = col - 1
        while up > 0 and left > 0 and self.board[up][left] == play*-1:
            up -= 1
            left -= 1
        if self.board[up][left] == play:
            if row > 0: up = row - 1
            if col > 0: left = col - 1
            while up > 0 and left > 0 and self.board[up][left] == play*-1:
                self.board[up][left] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                up -= 1
                left -= 1

        # check upper right
        if row > 0: up = row - 1
        if col < self.size - 1: right = col + 1 
        while up > 0 and right < self.size - 1 and self.board[up][right] == play*-1:
            up -= 1
            right += 1
        if self.board[up][right] == play:
            if row > 0: up = row - 1
            if col < self.size - 1: right = col + 1 
            while up > 0 and right < self.size - 1 and self.board[up][right] == play*-1:
                self.board[up][right] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                up -= 1
                right += 1

        # check down left
        if row < self.size - 1: down = row + 1
        if col > 0: left = col - 1
        while down < self.size - 1 and left > 0 and self.board[down][left] == play*-1:
            down += 1
            left -= 1
        if self.board[down][left] == play:
            if row < self.size - 1: down = row + 1
            if col > 0: left = col - 1
            while down < self.size - 1 and left > 0 and self.board[down][left] == play*-1:
                self.board[down][left] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                down += 1
                left -= 1

        # check down right
        if row < self.size - 1: down = row + 1
        if col < self.size - 1: right = col + 1 
        while down < self.size - 1 and right < self.size - 1 and self.board[down][right] == play*-1:
            down += 1
            right += 1
        if self.board[down][right] == play:
            if row < self.size - 1: down = row + 1
            if col < self.size - 1: right = col + 1 
            while down < self.size - 1 and right < self.size - 1 and self.board[down][right] == play*-1:
                self.board[down][right] = play
                if play == 1:
                    self.player += 1
                    self.computer -= 1
                else:
                    self.computer += 1
                    self.player -= 1
                down += 1
                right += 1





