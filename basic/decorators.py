__date__ = (8, 3, 2020)
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
