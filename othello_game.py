from othello_board import Board
from ai_player import AI

'''
    This is how the game runs! You are the player of this game!
'''

class Game(object):

    def __init__(self):
        print('New game starts!')
        print('-----------------------------------------------------')
        print('Now you could determine the board size and block numbers ~')
        print('-----------------------------------------------------')

        _input = input('Input the size of the board (Integers Only!!!!):')
        print('-----------------------------------------------------')
        self.size = self.input_int_detect(_input, 0, 100)


        _input = input('Input the number of blocks on the board (Integers Only!!!!):')
        print('-----------------------------------------------------')
        self.block = self.input_int_detect(_input, 0, self.size)

        self.ai_option = 1
        self.AI_RANDOM = 1
        self.AI_MINIMAX = 2
        self.AI_EXPECTIMAX = 3

        print('Now, choose the mode of game. 1:Easy mode(Random AI). 2:Medium mode(Minimax). 3:Hard mode(EXPECTIMAX)')
        print('-----------------------------------------------------')
        _input = input('Input the integer to the mode: ')
        print('-----------------------------------------------------')
        self.ai_option = self.input_int_detect(_input, 1, 4)

        print('Choose whether to play first')
        print('-----------------------------------------------------')
        who_first = input('input Y or N: ')
        print('-----------------------------------------------------')

        if who_first == 'Y':
            self.player = 1
        elif who_first == 'N':
            self.player = -1
        else:
            print('Your input is wrong, now you need to play first')
            print('-----------------------------------------------------')
            self.player = 1


        self.winner = 0
        self.NOT_FINISH = -1
        self.PLAYER_WIN = 1
        self.AI_WIN = 2


        print(' Hints : 2 is wall, 1 is you and -1 is AI')
        print('-----------------------------------------------------')
        self.oth = Board(self.size, self.block)
        self.oth.print_board()
        print('-----------------------------------------------------')

        self.game_begin()

    def input_int_detect(self, _input, start, end):
        while True:
            try:
                nint = int(_input)

                if nint >= start and nint  < end:
                    break
                else:
                    print('Your input is out of range!')
                    print('-----------------------------------------------------')
                    _input = input('You need to re-input a Integer number!!!')
                    print('-----------------------------------------------------')
            except:
                print('You did not input a Integer number!!!')
                print('-----------------------------------------------------')
                _input = input('You need to re-input a Integer number!!!')
                print('-----------------------------------------------------')

        return nint

    def player_turn(self, actions):
        print('Now you have several valid actions to choose')
        print('-----------------------------------------------------')
        print(actions)
        print('-----------------------------------------------------')
        print(' Hints : 2 is wall, 1 is you and -1 is AI')
        print('-----------------------------------------------------')

        while True:
            _input = input(
                'Input the index(from zero) you want to choose(Integers Only and must be less than {}):'.format(len(actions)))
            print('-----------------------------------------------------')

            index = self.input_int_detect(_input, 0, len(actions))
            action = actions[index]
            self.oth.player_action(action)
            print('Ok, now the board has changed:')
            print('-----------------------------------------------------')
            print('You could also withdraw this step, would you?')
            print('-----------------------------------------------------')
            _input = input('Input YES if you need to').capitalize()
            print('-----------------------------------------------------')
            if _input == 'YES':
                self.oth.backward()
            else:
                break

        self.oth.print_board()
        print('-----------------------------------------------------')

    def ai_turn(self, actions):
        print('Now it is the AI turn')
        print('-----------------------------------------------------')
        print('Valid actions:', actions)
        print('-----------------------------------------------------')

        if self.ai_option == self.AI_RANDOM:
            action = AI.random_method(actions)
        elif self.ai_option == self.AI_MINIMAX:
            action = AI.minimax_method(actions, self.oth)
        else:
            action = AI.expectimax_method(actions, self.oth)

        print("The AI chooses " + str(action))

        self.oth.ai_action(action)
        self.oth.print_board()
        print('-----------------------------------------------------')

    def game_begin(self):
        while True:
            actions = self.oth.action_valid(self.player)
            self.winner = self.oth.finish(actions)

            if self.winner == self.NOT_FINISH:
                if self.player == self.oth.PLAYER_COLOR:
                    self.player_turn(actions)
                else:
                    self.ai_turn(actions)

                self.player *= -1
            else:
                self.game_over()
                break

    def game_over(self):
        print('Okay, game over = 3 = ')
        print('-----------------------------------------------------')
        if self.winner == self.PLAYER_WIN:
            print('Great !!! You Win!!!!')
        elif self.winner == self.AI_WIN:
            print('Oops ..Sorry, good Luck next time!')
        else:
            print('Not bad, you are as smart as AI!')