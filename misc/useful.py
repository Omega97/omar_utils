"""
Collection of useful 'implement once' methods
"""


def loop_range(length: int, n: int, start=0, step=1):
    """range, but loop once index is over length"""
    for i in range(n):
        yield (start + i * step) % length


def loop_iter(v, n: int, start=0, step=1):
    """like range but loop instead of stopping at the end"""
    for i in range(n):
        j = (start + i * step) % len(v)
        yield v[j]


def q_print(v, pre_print=''):
    """print iterable"""
    if pre_print is not None:
        print(pre_print)
    for i in v:
        print(i)


def nested_print(x, depth=-1):
    """print with indentation, more nested = more indentation"""
    if hasattr(x, '__iter__') and type(x) != str:
        for i in x:
            nested_print(i, depth=depth+1)
    else:
        print('\t' * depth, end='')
        print(x)


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
        for i in generator(*args):
            yield (i,)
    else:
        for i in generator(*args):
            for j in recursive_iter(depth - 1, args=args, generator=generator):
                yield (i,) + j


if __name__ == '__main__':
    V = ['a', 'b', 'c']
    q_print(loop_range(10, 10, -1, 2))
    q_print(loop_iter(V, 10, -1))
    q_print(recursive_iter(3, 2))
