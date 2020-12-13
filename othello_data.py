from ai_with_ai import AI_WITH_AI

import torch as tr
import pickle as pk
import ai_net as an
import csv

''' 
    This is a file to generate data, include CSV file and PKL data.
'''

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

def write_csv_file(results, size):
    csvfile = open("csv/minimax_cnn_results%d.csv" % size, 'w', encoding='utf-8')
    #keys = ['index', 'random_nodes', 'minimax_nodes', 'random_score', 'minimax_score', 'winner']
    keys = ['index', 'minimax_actions', 'cnn_actions', 'minimax_score', 'cnn_score', 'winner', 'final_score']
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(keys)

    for result in results:
        writer.writerow(result)
    csvfile.close()

def write_pkl_file(data,size):
    inputs = []
    outputs = []
    for each in data:
        inputs.append(encode(each[0]))
        outputs.append(each[1])

    inputs = tr.stack(inputs)
    outputs = tr.tensor(outputs).float()
    outputs = tr.reshape(outputs, (len(outputs), 1))
    #print(inputs[-10:], outputs[-10:])
    with open("data/data%d.pkl" % size, "wb") as f: pk.dump((inputs, outputs), f)


def ai_random_with_minimax(size):
    results = []
    for i in range(0, 100):
        print('----No.', i, '----')
        test = AI_WITH_AI(size, i, None)
        test.random_minimax_game_begin()
        results.append(test.get_result())
    write_csv_file(results, size)

def ai_minimax_with_cnn(size):
    net = an.BlockusNet1(size)
    net.load_state_dict(tr.load("model/model%d.pth" % size))
    results = []
    for i in range(0, 100):
        print('----No.', i, '----')
        test = AI_WITH_AI(size, i, net)
        test.minimax_cnn_game_begin()
        results.append(test.get_result())
    write_csv_file(results, size)


def ai_minimax_with_minimax(size):
    data = []
    for i in range(0, 100):
        print('----No.', i,'----')
        test = AI_WITH_AI(size, i, None)
        test.minimax_minimax_game_begin()
        data.extend(test.get_data())

    write_pkl_file(data, size)


if __name__ == "__main__":
    #print('----No.', i,'----')ai_minimax_with_minimax(size=12)
    ai_minimax_with_cnn(size=11)


