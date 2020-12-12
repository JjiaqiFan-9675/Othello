from ai_with_ai import AI_WITH_AI

import torch as tr
import pickle as pk
import csv

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
    csvfile = open("csv/results_size"+size+"csv", 'w', encoding='utf-8')
    keys = ['index', 'random_nodes', 'minimax_nodes', 'random_score', 'minimax_score', 'winner']
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
    with open("/data/data%d.pkl" % size, "wb") as f: pk.dump((inputs, outputs), f)


def ai_random_with_minimax(size):
    results = []
    for i in range(0, 100):
        test = AI_WITH_AI(size, i)
        results.append(test.get_result())
    write_csv_file(results, size)


def ai_minimax_with_minimax(size):
    data = []
    for i in range(0, 100):
        print('----No.', i,'----')

        test = AI_WITH_AI(size, i)
        data.extend(test.data)

    write_pkl_file(data, size)


if __name__ == "__main__":
    ai_minimax_with_minimax(size=12)


