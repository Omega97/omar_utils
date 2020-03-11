"""         iter utils

Common tools to handle iterator
"""
__author__ = "Omar Cusma Fait"
__date__ = (11, 3, 2020)
__version__ = '1.3.0'

from time import time


def q_print(itr, n=0):
    """print an iterable (first n elements) """
    for i, x in enumerate(itr):
        print(x)
        if i + 1 == n:
            return


def gen_next_n(itr, n):
    """generator of next n items when called"""
    if n == 0:
        return
    for i, x in enumerate(itr):
        yield x
        if i + 1 == n:
            return


def one_in_n(itr, n):
    """yields only one element every n"""
    for i, x in enumerate(itr):
        if i % n == 0:
            yield x


def filter_iter(itr, criterion):
    """yields only elements of itr that match the criterion"""
    for i in itr:
        if criterion(i):
            yield i


def skip_n(itr, n):
    """skip n elements of itr """
    for i, x in enumerate(itr):
        if i >= n:
            yield x


def read_file(path, encoding='utf-8'):
    """read file line """
    with open(path, encoding=encoding) as file:
        for line in file:
            if line != '\n':
                yield line[:-1] if line[-1] == '\n' else line


# ---- less used ----------------------------------------------------------------


def count_outputs(itr):
    """yield dict of {output: number_of_occurrences}"""
    dct = {}
    for i in itr:
        dct[i] = 1 if i not in dct else dct[i] + 1
        yield dct


def gen_apply(itr, f):
    """apply f on elements of itr"""
    for i in itr:
        yield f(i)


def loop_range(length: int, n: int, start=0, step=1):
    """range, but loop once index is over length"""
    for i in range(n):
        yield (start + i * step) % length


def loop_list(v: list, n: int, start=0, step=1):
    """like range but loop instead of stopping at the end"""
    for i in range(n):
        j = (start + i * step) % len(v)
        yield v[j]


def loop_gen(constructor, *ag, **kw):
    """transform constructor into periodic generator
    constructor(*ag, **kw) must be iterable"""
    while True:
        for i in constructor(*ag, **kw):
            yield i


def split_data(itr, p):
    """
    splits elements of itr in 2 groups
    yields (1, element) with frequency p
    yields (0, element) with frequency 1-p
    :param itr: iterable
    :param p: proportion (frequency)
    """
    count = 0
    for i in enumerate(itr):
        n, x = i
        if count/(n+1) >= p:
            yield (0, x)
        else:
            yield (1, x)
            count += 1


def infinite_range():
    """like range, but never ends"""
    n = 0
    while True:
        yield n
        n += 1


# ---- time ----------------------------------------------------------------


def yield_time():
    """yield time lapsed from init"""
    t0 = time()
    while True:
        yield time() - t0


def yield_clock(itr, period):
    """yield periodically, only after "period" of time"""
    t = time()
    for i in itr:
        if time() - t > period:
            t += period
            yield i


# ---- SPECIAL ----------------------------------------------------------------


def recursive_iter(depth, args=None, generator=None):
    """
    iterate recursively (nested "for" loops)
    :param depth: number of nested loops
    :param args: args that go in range()
    :param generator: range by default, can be any generator
    """
    args = tuple() if args is None else args
    generator = range if generator is None else generator

    if depth <= 1:
        for i in generator(args):
            yield (i,)
    else:
        for i in generator(args):
            for j in recursive_iter(depth - 1, args=args, generator=generator):
                yield (i,) + j


def tensor_gen(shape):
    """yields tuples of indices that range from 0 to shape[i]-1
    Example:
        tensor_gen((3, 2))
        returns
        (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)
    """
    if shape:
        for i in range(shape[0]):
            for j in tensor_gen(shape[1:]):
                yield (i, ) + j
    else:
        yield tuple()


# -------------------------------------------------------------------


def gen_next_n_decorator(n):
    """the decorated methods yield only n times (n > 0)"""
    def wrap1(fun):
        def wrap2(*a, **kw):
            j = n
            for i in fun(*a, **kw):
                yield i
                j -= 1
                if not j:
                    break
        return wrap2
    return wrap1


def one_in_n_decorator(n):
    """the decorated methods yield only once every n times"""
    def wrap1(fun):
        def wrap2(*a, **kw):
            j = n
            for i in fun(*a, **kw):
                j -= 1
                if not j:
                    yield i
                    j = n
        return wrap2
    return wrap1


# ---- TESTS ----------------------------------------------------------------


def wrap_itr(itr, fun):
    """wrap fun around iterable"""
    for i in itr:
        yield fun(i)


def __test_the_important_ones():
    a = infinite_range()
    a = skip_n(a, 2)
    a = one_in_n(a, 4)
    assert list(gen_next_n(a, 4)) == [2, 6, 10, 14]
    assert list(gen_next_n(a, 2)) == [18, 22]


def __test_count_outputs():
    v = [1, 1, 1, 2, 2, 4]
    assert list(count_outputs(v))[-1] == {1: 3, 2: 2, 4: 1}


if __name__ == '__main__':
    __test_the_important_ones()
    __test_count_outputs()
