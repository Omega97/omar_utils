""" lib of useful functions
4/3/2019
"""
from math import exp, tanh


# todo add derivative


def module(v):
    return sum([i**2 for i in v])**.5


def dist(v, w=None):
    if w is None:
        return module(v)
    else:
        return sum([(v[i] - w[i])**2 for i in range(len(v))])**.5


def poly(x, coefficients):
    return sum([x ** n * coefficients[n] for n in range(len(coefficients))])


def sigmoid(x):
    return 1/(1 + exp(-x))


def th(x):
    return tanh(x)


def step(x, der=False):
    return x >= 0 * der


def relu(x, der=False):
    return max(x, 0) if not der else step(x)


def prelu(x, p=0., der=False):
    assert 0. <= p <= 1.
    return max(x, p * x) if not der else max(1., p)


def product(v):
    """ return function, product of all functions in v """
    def f(x):
        out = 1
        for i in v:
            out *= i(x)
        return out
    return f


if __name__ == "__main__":

    assert module([3, 4]) == 5
    assert dist([-2, -2], [1, 2]) == 5
    assert poly(2, [1, -1, 2]) == 7
    assert step(2) == 1
    assert relu(2) == 2
    assert relu(-2) == 0

    assert prelu(2, .1) == 2
    assert prelu(-2, .1) == -.2
