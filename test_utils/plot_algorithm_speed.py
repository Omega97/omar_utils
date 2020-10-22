"""
                plot_algorithm_speed

Compare time it takes to execute a list of algorithms
"""
import matplotlib.pyplot as plt
import numpy as np
from time import time


def get_time(f):
    t = time()
    f()
    return time() - t


def test_time(algorithms: list, repeat=2, title='Time comparison', y_label='s'):
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
