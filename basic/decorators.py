__date__ = (8, 3, 2020)     # debug
from time import time


def take_time(fun):
    """measure the time it takes to execute fun"""
    def wrapper(*args, **kwargs):
        t0 = time()
        fun(*args, **kwargs)
        return time() - t0
    return wrapper


def take_average_time(n):
    """ generate a decorator that measures the time it takes to execute fun (average over n times) """
    def wrapper1(fun):
        def wrapper2(*args, **kwargs):
            t = time()
            for _ in range(n):
                fun(*args, **kwargs)
            return (time() - t) / n
        return wrapper2
    return wrapper1


def debug(fun):
    def wrap(*args, **kwargs):
        s = f'{fun.__name__}('
        if len(args):
            s += f'{", ".join([str(i) for i in args])}'
        if len(kwargs):
            s += f', {", ".join([str(i) + "=" + str(kwargs[i]) for i in kwargs])}'
        s += ')'
        print(s, '...')
        out = fun(*args, **kwargs)
        s += f' -> {out}'
        print(s)
        return out
    return wrap


class Debug:

    count = 0

    def __call__(self, fun):
        def wrap(*args, **kwargs):
            s = f'{fun.__name__}('
            if len(args):
                s += f'{", ".join([str(i) for i in args])}'
            if len(kwargs):
                s += f', {", ".join([str(i) + "=" + str(kwargs[i]) for i in kwargs])}'
            s += ')'
            print('|\t' * (Debug.count))
            print('|\t' * Debug.count, s)
            Debug.count += 1
            out = fun(*args, **kwargs)
            s = f'{out}'
            Debug.count -= 1
            print('|\t' * (Debug.count + 1))
            print('|\t' * Debug.count, s)
            return out
        return wrap


if __name__ == '__main__':

    @take_average_time(10)
    def f(n):
        return [i for i in range(n)]

    print(f(10**5))
