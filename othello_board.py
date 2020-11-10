import numpy as np
import random


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
        self.last_player_node = self.player_node
        self.last_ai_node = self.ai_node


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

    def action_valid(self, player):
        actions = set()

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player * -1:
                    for (x,y) in [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]:
                        _row, _col = i+x*-1, j+y*-1

                        if _row < 0 or _col < 0 or _row >= self.size or _col >= self.size:
                            continue

                        nrow, ncol = i, j
                        while self.board[nrow][ncol] == player*-1:
                            nrow += x
                            ncol += y
                            if nrow < 0 or ncol < 0 or nrow >= self.size or ncol >= self.size:
                                break

                        if nrow < 0 or ncol < 0 or nrow >= self.size or ncol >= self.size:
                            continue

                        if self.board[nrow][ncol] == player and self.board[_row][_col] == self.EMPTY:
                            actions.add((i+x, j+y))

        return list(actions)

    # Player is 1
    def player_action(self, action):
        self.last_ai_node = self.ai_node
        self.last_player_node = self.player_node
        self.last_board_state = self.board.copy()

        self.change(action,self.PLAYER_COLOR)
        self.board[action[0]][action[1]] = self.PLAYER_COLOR
        self.player_node += 1

    # AI is -1
    def ai_action(self, action):
        self.last_ai_node = self.ai_node
        self.last_player_node = self.player_node
        self.last_board_state = self.board.copy()

        print("The AI chooses " + str(action))
        self.change(action, self.AI_COLOR)
        self.board[action[0]][action[1]] = self.AI_COLOR
        self.ai_node += 1

    def backward(self):
        self.ai_node = self.last_ai_node
        self.player_node = self.last_player_node
        self.board = self.last_board_state.copy()

    def print_board(self):
        print(self.board)

    # if player win, return 1;
    # if computer win, return 2;
    # if both win, return 0;
    # if game not finished, return -1;
    def finish(self, actions):
        if self.block + self.player_node + self.ai_node == self.size * self.size or len(actions) == 0:
            if self.player_node > self.ai_node: return 1
            elif self.player_node < self.ai_node: return 2
            else: return 0

        return -1

    def change(self, action, player):
        row = action[0]
        col = action[1]

        for (x, y) in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]:
            # check if this player was surrounded by other player
            nrow, ncol = row+x, col+y
            if nrow < 0 or ncol < 0 or nrow >= self.size or ncol >= self.size:
                continue

            while self.board[nrow][ncol] != self.WALL:
                nrow, ncol = nrow + x, ncol + y
                if nrow < 0 or ncol < 0 or nrow >= self.size or ncol >= self.size:
                    break

            if nrow > -1 and ncol > -1 and nrow < self.size and ncol < self.size:
                continue

            if self.board[nrow][ncol] == self.WALL:
                continue

            nrow, ncol = row + x, col + y
            while self.board[nrow][ncol] == player*-1:
                self.board[nrow][ncol] = player

                if player == self.PLAYER_COLOR:
                    self.player_node += 1
                    self.ai_node -= 1
                else:
                    self.player_node -= 1
                    self.ai_node += 1

                nrow, ncol = nrow + x, ncol + y
                if nrow < 0 or ncol < 0 or nrow >= self.size or ncol >= self.size:
                    break





