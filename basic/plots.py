""" plot heat-map and heat-map gif """
import matplotlib.pyplot as plt
import numpy as np
from omar_utils.basic.tensors import is_matrix, tensor_max, tensor_min


plt.rcParams.update({'figure.max_open_warning': -1})    # removes memory limits


def matrix_to_heatmap(mat, title="Heat-map", cmap='hot', interpolation=None, show=True):
    """ show dec heat-map of the given matrix """
    if not is_matrix(mat):
        raise TypeError('Argument is not dec matrix!')

    plt.imshow(mat, cmap=cmap, interpolation=interpolation)
    if title:
        plt.title(title)

    if show:
        plt.show()


def matrix_to_heatmap2(mat, n_labels=None, title="Heat-map", cmap='hot',  # todo upside down?
                       x_range=None, y_range=None, z_range=None, show=True, interpolation=None):
    """ show dec heat-map of the given matrix
    cmap: 'hot', 'viridis', 'gray', ...
    interpolation: 'bicubic', ...
v    """

    if not is_matrix(mat):
        raise TypeError('Argument is not dec matrix!')

    # orient it properly
    mat = [mat[i] for i in range(len(mat)-1, -1, -1)]

    # init plot
    fig, ax = plt.subplots()
    z_range = z_range if z_range else [tensor_min(mat), tensor_max(mat)]

    try:
        ax.imshow(mat, cmap=cmap, vmin=z_range[0], vmax=z_range[1], interpolation=interpolation)
    except TypeError:
        print(mat, '\n')
        raise TypeError

    ax.set_xticks(np.arange(len(mat)))
    ax.set_yticks(np.arange(len(mat[0])))
    plt.gca().invert_yaxis()

    # labels
    x_range = x_range if x_range else [0, len(mat) - 1]
    y_range = y_range if y_range else [0, len(mat[0]) - 1]
    x_labels = ['' for _ in range(len(mat))]
    y_labels = ['' for _ in range(len(mat[0]))]
    n_labels = n_labels if n_labels else 0
    for i in range(n_labels):
        n_x = round((len(mat)-1) * i/(n_labels-1))
        n_y = round((len(mat[0])-1) * i/(n_labels-1))
        x_labels[n_x] = x_range[0] + (x_range[1] - x_range[0]) / (len(mat) - 1) * n_x
        y_labels[n_y] = y_range[0] + (y_range[1] - y_range[0]) / (len(mat[0]) - 1) * n_y
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    ax.set_title(title)

    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    if show:
        plt.show()

    return image


def plots_to_slide(list_, x=None, y=None):  # todo finish
    """ show slide of plots given list of plots """
    x = x if x else 4
    y = y if y else round(y / x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Simple plot')

    for i in range(len(list_)):
        plt.subplot(2, 1, 2)
        plt.plot(list_[i])

    plt.show()


# todo correct empty spaces
def tensor_to_slide(list_, nrows=None, n_cols=None, z_range=None, interpolation='quadric', cmap=None):
    """ show slide of heat-map plots given tensor """
    # init canvas, matrix of subplots

    if nrows is None and n_cols is None:
        for i in range(round(len(list_) ** .5)):
            n_cols = 4

    if nrows is None:
        nrows = len(list_) // n_cols + (0 if len(list_) % n_cols == 0 else 1)

    if n_cols is None:
        n_cols = len(list_) // nrows + (0 if len(list_) % nrows == 0 else 1)

    z_range = z_range if z_range else [tensor_min(list_), tensor_max(list_)]

    fig, axs = plt.subplots(nrows=nrows, ncols=n_cols, figsize=(9, 6), subplot_kw={'xticks': [], 'yticks': []})

    for i in range(len(axs.flat)):  # matrix -> array
        if i >= len(list_):
            break
        axs.flat[i].imshow(list_[i], interpolation=interpolation, vmin=z_range[0], vmax=z_range[1], cmap=cmap)

    plt.tight_layout()
    plt.show()


# todo improve
def simple_plot(*args, show=True, color=None, title=None):
    """ simple 1D plot """
    if len(args) == 1:
        y, = args
        if type(y) == list:
            x = np.arange(0, len(y))
            plt.plot(x, y, color=color)
        else:
            x = np.arange(-5, 5, .2)
            plt.plot(x, [y(i) for i in x], color=color)
    elif len(args) == 2:
        x, y = args
        if type(y) == list:
            plt.plot(x, y, color=color)
        else:
            plt.plot(x, [y(i) for i in x], color=color)
    else:
        return

    plt.title(title)

    if show:
        plt.show()


if __name__ == "__main__":

    from random import randrange

    T = [[randrange(12) for _ in range(10)] for _ in range(5)]
    matrix_to_heatmap(T, show=True, interpolation=None)
