from copy import deepcopy
import numpy as np


def simple_gradient(dx=10 ** -9):
    def wrapper(f, x0):
        """gradient of f in v (dx = tiny step to compute derivatives) (2 n calls of f)"""
        return np.array([(f([x0[j] + dx * (i == j) for j in range(len(x0))]) -
                          f([x0[j] - dx * (i == j) for j in range(len(x0))])) / (2 * dx) for i in range(len(x0))])
    return wrapper


def fast_gradient(dx=10 ** -9):
    def wrapper(f, x0, cost0=None):
        """gradient of f in v (recycle cost0) (n + 1 calls of f)"""
        if cost0 is None:
            cost0 = f(x0)
        return np.array([(f([x0[j] + dx * (i == j) for j in range(len(x0))]) - cost0) / dx for i in range(len(x0))])
    return wrapper


class Optimizer:
    """Optimizer"""

    def __init__(self):
        self.loss = None
        self.grad_method = None
        self.sol = None
        self.steps = 0
        self.cost = None
        self.data = []
        self.converged = False
        self.grad_method = None

    def compile(self, loss=None, gradient=None):
        if loss:
            self.loss = loss
        self.grad_method = gradient if gradient is not None else fast_gradient()

    def init_fit(self, initial_point):
        """set standard initial parameters for fit"""
        self.sol = deepcopy(initial_point)
        self.data = []
        self.steps = 0
        self.cost = None
        self.converged = False

    def keep_iter(self, n_steps, min_cost):
        """standard protocol used when deciding weather to keep iterating fit or not"""
        self.steps += 1
        self.data.append(deepcopy(self.sol))
        self.cost = self.loss(self.sol)
        if min_cost is not None:
            if self.cost <= min_cost:
                # model converged
                self.converged = True
                self.sol = [float(i) for i in self.sol]     # convert back to python float
                return False
        if self.steps >= n_steps:
            # too many steps
            self.sol = [float(i) for i in self.sol]     # convert back to python float
            return False
        return True

    def gradient(self, x):
        return self.grad_method(self.loss, x)


class GradientDescent(Optimizer):
    """GD"""
    def __init__(self):
        super().__init__()

    def fit(self, initial_point, n_steps=100, min_cost=None, eta=.1, k=0.):
        """training"""
        self.init_fit(initial_point)
        while self.keep_iter(n_steps, min_cost):
            # compute gradient and update solution
            self.sol = self.sol - eta * self.gradient(self.sol)
            eta *= (1-k)


class RProp(Optimizer):
    """RProp"""
    def __init__(self):
        super().__init__()

    def fit(self, initial_point, n_steps=100, min_cost=10**-5, s0=.1, k_plus=4/3, k_minus=1/3):
        """training"""
        self.init_fit(initial_point)

        # init speed & gradient
        grad = self.gradient(self.sol)
        speed = [s0 for _ in range(len(self.sol))]

        while self.keep_iter(n_steps, min_cost):
            # compute gradient
            new_grad = self.gradient(self.sol)

            new_speed = [i for i in speed]

            for i in range(len(self.sol)):
                if new_grad[i] * grad[i] > 0:  # keep going
                    new_speed[i] *= k_plus
                    self.sol[i] -= np.sign(new_grad[i]) * new_speed[i]
                elif new_grad[i] * grad[i] < 0:  # step back
                    new_speed[i] *= k_minus
                    new_grad[i] = 0
                else:
                    self.sol[i] -= np.sign(new_grad[i]) * new_speed[i]

            grad = new_grad
            speed = new_speed


class RPropPlus(Optimizer):
    """RPropPlus"""
    def __init__(self):
        super().__init__()

    def fit(self, initial_point=None, n_steps=100, min_cost=10**-5, s0=.1, k_plus=4/3, k_minus=1/3):
        """training"""
        if initial_point is None:
            initial_point = self.sol
        self.init_fit(initial_point)

        # init gradient & speed
        grad = self.gradient(self.sol)
        speed = [max(abs(i * s0), s0 / 10) for i in grad]

        while self.keep_iter(n_steps, min_cost):
            # compute gradient
            new_grad = self.gradient(self.sol)

            new_speed = [i for i in speed]
            new_sol = deepcopy(self.sol)
            delta = [0. for _ in speed]

            for i in range(len(self.sol)):
                if new_grad[i] * grad[i] > 0:  # keep going
                    new_speed[i] *= k_plus
                    delta[i] = -np.sign(new_grad[i]) * new_speed[i]
                    new_sol[i] = self.sol[i] + delta[i]
                elif new_grad[i] * grad[i] < 0:  # slow down
                    new_speed[i] *= k_minus
                    new_grad[i] = 0
                else:
                    delta[i] = -np.sign(new_grad[i]) * new_speed[i]
                    new_sol[i] = self.sol[i] + delta[i]

            new_cost = self.loss(new_sol)

            if new_cost <= self.cost:
                # better solution
                grad = new_grad
                speed = new_speed
                self.cost = new_cost
                self.sol = new_sol
            else:
                # step back
                speed = [i * k_minus for i in speed]


if __name__ == '__main__':

    from math import *

    def test_loss(v):
        return sum(i**2 for i in v)

    for alg in [GradientDescent, RProp, RPropPlus]:
        optimizer = alg()
        optimizer.compile(loss=test_loss)
        optimizer.fit(initial_point=[2, 1], min_cost=10**-6)
        print(optimizer.steps)
        print(optimizer.sol)
        print(optimizer.cost)
        print()
