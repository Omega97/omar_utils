from test_utils.debug import *


def example_1():
    """simple nested functions"""

    @Debug
    def f(x):
        return x + 1

    @Debug
    def g(x):
        return f(x + 1)

    g(1)


def example_2():    # todo generators
    """"""

    @Debug
    def f(n, p=2):
        for i in range(n):
            yield i**p

    @Debug
    def g(n):
        return sum(f(n))

    g(1)


if __name__ == '__main__':
    example_1()
