"""         iter utils

Common tools to handle iterator
"""
__author__ = "Omar Cusma Fait"
__date__ = (3, 3, 2020)
__version__ = '1.3.0'

from time import time


def q_print(item, n=None):
    """print an iterator (first n elements if n is defined) """
    print()
    for i in item:
        if n is not None:
            n -= 1
            if n < 0:
                return
        print(i)


def gen_next_n(itr, n):
    """generator of next n items when called"""
    for i in itr:
        n -= 1
        if n < 0:
            break
        yield i


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


def one_in_n(itr, n):
    """yields only one element every n"""
    j = n
    for i in itr:
        j -= 1
        if not j:
            yield i
            j = n


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


def filter_iter(itr, criterion):
    """yields only elements of itr that match the criterion"""
    for i in itr:
        if criterion(i):
            yield i


def skip_n(itr, n):
    """skip n elements of itr """
    for i in itr:
        if n <= 0:
            yield i
        n -= 1


# ---- less used ----------------------------------------------------------------


def count_outputs(itr):
    """yield dict of {output: number_of_occurrences}"""
    dct = {}
    for i in itr:
        dct[i] = 1 if i not in dct else dct[i] + 1
        yield dct


def cond_gen(itr, cond):
    """yield only when condition is met"""
    for i in itr:
        if cond(i):
            yield i


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


def get_time_iter(itr):
    """:returns time it takes to iter over itr"""
    t0 = time()
    for _ in itr:
        pass
    return time() - t0


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


# ---- TESTS ----------------------------------------------------------------

def wrap_itr(itr, fun):
    """wrap fun around iterable"""
    for i in itr:
        yield fun(i)


def __test_the_important_ones():
    def inf_range():
        n = 0
        while True:
            yield n
            n += 1

    a = inf_range()
    a = skip_n(a, 1)
    a = one_in_n(a, 5)
    a = gen_next_n(a, 5)
    q_print(a)


def __test_count_outputs():
    v = [1, 1, 1, 2, 2, 4]
    q_print(count_outputs(v))


def __test_yield_clock():
    a = (yield_clock(yield_time(), .25))
    a = wrap_itr(a, lambda x: f'{x:.3f} s')
    a = gen_next_n(a, 4)
    q_print(a)


if __name__ == '__main__':
    __test_the_important_ones()
    __test_count_outputs()
    __test_yield_clock()
