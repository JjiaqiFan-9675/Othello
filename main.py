
from Othello import Othello

def game_begin():
    print('New game starts!')

    try:
        size = int(input('Input the size of the board (Integers Only!!!!):'))
        block = int(input('Input the number of blocks on the board (Integers Only!!!!):'))
    except:
        print('You did not input a number, now game starts with 8*8 board and 3 blocks')
        size = 8
        block = 3

    print('-----------------------------------------------------')
    print('Choose whether to play first')
    first = input('input Y or N: ')

    if first == 'Y' : play = 1
    elif first == 'N' : play = -1
    else:
        print('Your input is wrong, now you need to play first')
        play = 1

    print('-----------------------------------------------------')
    print(' Hints : 2 is wall, 1 is you and -1 is AI')
    oth = Othello(size, block)
    oth.print_board()

    while True:
        actions = oth.action_valid(play)
        isfinish = oth.finish(actions)
        if isfinish < 0:
            if play == 1:
                print('-----------------------------------------------------')
                print('Now you have several valid actions to choose')
                print(actions)
                indexIn = input('Input the index you want to choose(Integers Only and must be less than {}):'.format(len(actions)))

                index = int(indexIn) -1
                if index >= size or index < 0:
                    print('Your input is inValid. You determined to choose the first one.')
                    index = 0
                action = actions[index]
                oth.player_action(action)
                oth.change(action, play)
                print('Ok, now the board has changed:')
                oth.print_board()
            else:
                print('-----------------------------------------------------')
                print('Now it is the AI turn')
                print('Valid actions:', actions)
                oth.computer_action(actions)
                oth.print_board()
            play *= -1
        else:
            print('-----------------------------------------------------')
            print('Okay, game over = 3 = ')
            if isfinish == 1:
                print('Great !!! You Win!!!!')
            elif isfinish == 2:
                print('Oops ..Sorry, good Luck next time!')
            else:
                print('Not bad, you are the same as AI!')
            break

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game_begin()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
