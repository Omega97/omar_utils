""" lib of useful functions
26/2/2019
"""

# todo add derivative

from math import exp, tanh


def poly(x, coefficients):
    return sum([x ** n * coefficients[n] for n in range(len(coefficients))])


def sigmoid(x):
    return 1/(1 + exp(-x))


def th(x):
    return tanh(x)


def relu(x):
    return max(x, 0)


def prelu(x, p=0.):
    return max(x, p * x)


if __name__ == "__main__":
    ...
