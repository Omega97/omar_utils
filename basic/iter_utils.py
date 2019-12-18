"""         iter_utils

Most common tools to handle iterator
"""
__author__ = "Omar Cusma Fait"
__date__ = (17, 12, 2019)
__version__ = '1.0.1'

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


def skip_n(gen, n):
    """skip n elements of gen (instantaneous!)"""
    for _ in range(n):
        try:
            next(gen)
        except StopIteration:
            pass
    return gen


def gen_first_n_items(gen, n):
    """return n items of gen (if possible)"""
    for i in gen:
        n -= 1
        yield i
        if n <= 0:
            return


def to_list(gen):
    """returns function that returns list of first n items of gen"""
    def f(n=None):
        if n is None:
            return list(gen)
        else:
            return list(gen_first_n_items(gen, n))
    return f


def gen_split_string(gen):
    """yield list of int (if possible, else keep str)"""
    for i in gen:
        yield [j for j in i.split()]


def gen_list_to_int(gen):
    """yield list of int (if possible, else keep str)"""
    for i in gen:
        yield [int(j) for j in i]


def get_time_iter(gen):
    """:returns time it takes to iter over gen"""
    t0 = time()
    for _ in gen:
        pass
    return time() - t0


def cond_gen(gen, cond):
    """yield only when condition is met"""
    for i in gen:
        if cond(i):
            yield i


def gen_apply(gen, f):
    """apply f on elements of gen"""
    for i in gen:
        yield f(i)

# ----------------------------------------------------------------


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


def loop_generator(fun, n=None):
    """iter over n elements yielded by fun(), restart each time last element is reached"""
    while True:
        for item in fun():
            if n is not None:
                n -= 1
                if n <= 0:
                    return
            yield item


def loop_range(length: int, n: int, start=0, step=1):
    """range, but loop once index is over length"""
    for i in range(n):
        yield (start + i * step) % length


def loop_list(v: list, n: int, start=0, step=1):
    """like range but loop instead of stopping at the end"""
    for i in range(n):
        j = (start + i * step) % len(v)
        yield v[j]


# ----------------------------------------------------------------


if __name__ == '__main__':

    def sample_gen():
        def f():
            with open('data.txt') as f:
                for i in f:
                    yield i
        return f()


    def gen_2_in_1(gen):
        """yield list of int (if possible, else keep str)"""
        for i in gen:
            yield [int(j) for j in i.split()]   # 2 in 1 30% better



    t = []

    data = sample_gen()
    t += [get_time_iter(data)]

    data = sample_gen()
    data = gen_split_string(data)
    t += [get_time_iter(data)]

    data = sample_gen()
    data = gen_split_string(data)
    data = gen_list_to_int(data)
    t += [get_time_iter(data)]

    data = sample_gen()
    data = gen_2_in_1(data)

    t += [get_time_iter(data)]

    data = sample_gen()
    data = gen_split_string(data)
    data = gen_list_to_int(data)
    data = skip_n(data, round(10000))
    t += [get_time_iter(data)]

    for I in t:
        print(round(I / t[0] * 10))
