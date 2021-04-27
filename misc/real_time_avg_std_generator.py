
def avg_std_gen(x_gen):
    """
    A generator that computes average and standard deviation as data come in,
    without memorizing the data-set in the process.
    Works also with numpy arrays

    :param x_gen: iterable of values
    :yields: (avg, std)

    formulas
    a' = (n * a + x') / n'
    v' = (n * (v + (a' - a)**2) + (x'-a')) / n'
    """

    def f_update(old, new, weight):
        return (old * weight + new) / (weight + 1)

    avg = var = 0.

    for n, new_x in enumerate(x_gen):
        old_avg = avg
        avg = f_update(avg, new_x, n)
        var = f_update(var + (avg  - old_avg) ** 2, (new_x - avg) ** 2, n)
        yield avg, var ** .5
