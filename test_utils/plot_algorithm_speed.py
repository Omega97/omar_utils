import matplotlib.pyplot as plt
import numpy as np
from time import time


def get_time(f):
    t = time()
    f()
    return time() - t


def test_time(algorithms: list, repeat=5, title='Time comparison', y_label='s'):
    """display a plot if time taken to execute algorithms"""
    data = [[] for _ in algorithms]

    # get times
    for i in range(repeat):
        for j in range(len(algorithms)):
            data[j].append(get_time(algorithms[j]))

    avg = [np.average(i) for i in data]
    std = [np.std(i) for i in data]

    plt.scatter(range(len(avg)), avg)
    plt.errorbar(range(len(avg)), avg, yerr=std, ls='none')
    plt.ylim(0.)
    plt.title(title)
    plt.ylabel(y_label)
    plt.show()


if __name__ == '__main__':
    from random import random

    def fun(n):
        def f():
            return sorted([random() for _ in range(n)])
        return f

    test_time([fun(i * 10**4) for i in range(10)])
