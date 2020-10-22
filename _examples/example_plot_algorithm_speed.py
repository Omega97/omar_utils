from test_utils.plot_algorithm_speed import *
from random import random


def example():

    def fun(n):
        def f():
            return sorted([random() for _ in range(n)])
        return f

    test_time([fun(2**i) for i in range(10, 17)])


if __name__ == '__main__':
    example()
