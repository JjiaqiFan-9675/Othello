from othello_game import Game
from ai_game_test import GameTest
import csv

othello_game = Game()

'''
    The following code is to test the efficiency of AI.
'''

def write_csv_file(results):
    csvfile = open("data/results_size20.csv", 'w', encoding='utf-8')
    keys = ['index', 'random_nodes', 'minimax_nodes', 'random_score', 'minimax_score', 'winner']
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(keys)

    for result in results:
        writer.writerow(result)
    csvfile.close()

def ai_ai(size):
    results = []
    for i in range(0,100):
        test = GameTest(size, i)
        results.append(test.get_result())
    write_csv_file(results)

