""" plot heat-map and heat-map gif """
import matplotlib.pyplot as plt
import numpy as np
import imageio
from omar_utils.tensors import is_matrix


plt.rcParams.update({'figure.max_open_warning': -1})    # removes memory limits


def matrix_to_heatmap(mat, n_labels=None, title="Heat-map", cmap='hot',
                      x_range=None, y_range=None, z_range=None, show=True):
    """ show a heat-map of the given matrix """

    if not is_matrix(mat):
        raise IndexError('mat is not a matrix')

    # orient it properly
    mat = [mat[i] for i in range(len(mat)-1, -1, -1)]

    # init plot
    fig, ax = plt.subplots()
    z_range = z_range if z_range else [0, 1]

    try:
        ax.imshow(mat, cmap=cmap, vmin=z_range[0], vmax=z_range[1])  #
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


def tensor_to_heatmap_gif(t, path='./my_gif.gif', fps=5, x_range=None, y_range=None, title='Lantern'):
    """ convert tensor to gif """
    imageio.mimsave(path,
                    [matrix_to_heatmap(i, x_range=x_range, y_range=y_range, title=title, show=False) for i in t],
                    fps=fps)


def plots_to_slide(list_):

    plt.subplot(2, 1, 1)
    plt.plot(list_[0])

    plt.subplot(2, 1, 2)
    plt.plot(list_[1])

    plt.show()


def tensor_to_slide(list_, nrows=None, ncols=None):
    # init canvas, matrix of subplots

    if nrows is None and ncols is None:
        for i in range(round(len(list_) ** .5)):
            ncols = 4

    if nrows is None:
        nrows = len(list_) // ncols + (0 if len(list_) % ncols == 0 else 1)

    if ncols is None:
        ncols = len(list_) // nrows + (0 if len(list_) % nrows == 0 else 1)

    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(9, 6), subplot_kw={'xticks': [], 'yticks': []})

    for i in range(len(axs.flat)):  # matrix -> array
        if i >= len(list_):
            break
        axs.flat[i].imshow(list_[i], interpolation='quadric')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    M = [[.1, .2], [.3, .4]]
    # matrix_to_heatmap(M)

    # GIF

    T = [[[.1, -.2], [-.3, .4]], [[.1, .2], [.3, .4]]]
    # tensor_to_heatmap_gif(T, fps=10)

    plots_to_slide([matrix_to_heatmap(M, show=False),
                    matrix_to_heatmap(M, show=False)])
