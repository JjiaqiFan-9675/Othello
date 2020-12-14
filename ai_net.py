import torch as tr
import numpy as np
import pickle as pk
from torch.nn import Linear, Flatten

'''
    This is to generate CNN model from PKL data.
    Each model uses 5000 iterations of gradient descent to train neural networks.
    The figure generated is in directory 'figure'
'''
def Aitong_Net(board_size):
    class Nets(tr.nn.Module):
        def __init__(self, board_size):
            super(Nets, self).__init__()
            self.flatten = Flatten(start_dim=1)
            self.linear = Linear(board_size ** 2 * 3, 1)

        def forward(self, input_value):
            temp = self.flatten(input_value)
            return self.linear(temp)

    return Nets(board_size)

def Jiaqi_Net(board_size):
    class Nets(tr.nn.Module):
        def __init__(self, board_size):
            super(Nets, self).__init__()
            self.conv1 = tr.nn.Conv2d(3, 1, 1)
            self.flatten = Flatten(start_dim=1)
            self.linear = Linear(board_size ** 2, 1)

        def forward(self, input_value):
            temp = self.conv1(input_value)
            temp = self.flatten(temp)
            return self.linear(temp)

    return Nets(board_size)

def calculate_loss(net, x, y_targ):
    temp = (net(x) - y_targ) ** 2
    return net(x), tr.sum(temp)

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    e.backward()
    optimizer.step()
    return y, e


if __name__ == "__main__":
    board_size = 12
    net = Jiaqi_Net(board_size=board_size)

    with open("data/data%d.pkl" % board_size, "rb") as f:
        (x, y_targ) = pk.load(f)

    # Optimization loop
    optimizer = tr.optim.Adam(net.parameters())
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 10
    train, test = shuffle[:-split], shuffle[-split:]
    for epoch in range(1000):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle) - split))
        test_loss.append(e_test.item() / split)

    tr.save(net.state_dict(), "model2/model%d.pth" % board_size)

    import matplotlib.pyplot as pt

    pt.plot(train_loss, 'b-')
    pt.plot(test_loss, 'r-')
    pt.legend(["Train", "Test"])
    pt.title("Resulting Learning Curve%d" % board_size)
    pt.xlabel("Iteration")
    pt.ylabel("Average Loss")
    #pt.savefig("figure/learning_curve%d.png" % board_size)
    pt.savefig("figure2/learning_curve%d.png" % board_size)
    pt.show()

    pt.plot(y_train.detach().numpy(), y_targ[train].detach().numpy(), 'bo')
    pt.plot(y_test.detach().numpy(), y_targ[test].detach().numpy(), 'ro')
    pt.legend(["Train", "Test"])
    pt.title("Target-Actual Scatter Plot%d" % board_size)
    pt.xlabel("Actual output")
    pt.ylabel("Target output")
    #pt.savefig("figure/scatter_plot%d.png" % board_size)
    pt.savefig("figure2/scatter_plot%d.png" % board_size)
    pt.show()