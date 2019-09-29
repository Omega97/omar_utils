import numpy as np
import matplotlib.pyplot as plt
from random import random


def ran():
    return random() - random()


def range_test(v):
    return sum([i < 0 for i in v]) == 0


def fill(loss, domain):
    def f(v):
        if domain(v):
            return loss(v)
        else:
            return 20
    return f


def add_noise(fun, k=.01):
    def f(*args, **kwargs):
        return fun(*args, **kwargs) + ran() * k
    return f


def plot_loss(loss, x_range, y_range, dx=.1, title=None, vmin=0, vmax=2):
    """plot loss space"""
    x_ = np.arange(x_range[0], x_range[1] + dx, dx)
    y_ = np.arange(y_range[1], y_range[0] - dx, -dx)

    data_ = np.array([[loss([x, y]) ** (1 / 5) for x in x_] for y in y_])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(data_,
              interpolation='bicubic',
              cmap='Blues',
              extent=[min(x_), max(x_), min(y_), max(y_)],
              vmin=vmin,
              vmax=vmax)
    period = 1
    ax.set_xticks([x for x in x_ if round(x/period, 8) == round(x/period)])
    ax.set_yticks([y for y in y_ if round(y/period, 8) == round(y/period)])
    plt.title(title)


def plot_path(points, color='blue'):
    """plot the path traced by 1 point in the parameter space"""
    x = [points[i][0] for i in range(len(points))]
    y = [points[i][1] for i in range(len(points))]

    plt.plot(x, y, c=color, linewidth=.3)
    for i in points:
        plt.plot(i[0], i[1], '+', color=color, markersize=2)
    plt.plot(points[-1][0], points[-1][1], 'o', color=color, markersize=2)


def plot_loss_and_paths(loss, optimizers, init_points, x_range, y_range, dx, fit_kwargs):
    """plot loss and path"""
    plot_loss(loss, x_range=x_range, y_range=y_range, dx=dx)

    colors = ['blue', 'red', 'green']

    for i in range(len(optimizers)):
        for p in init_points:
            model_ = optimizers[i](loss)
            model_.run(p, **fit_kwargs)
            data_ = model_.data
            plot_path(data_, color=colors[i % len(colors)])
            print(model_.steps)
            print(model_.cost)
    plt.show()
