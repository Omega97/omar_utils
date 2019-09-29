""" Timer

- initialize a timer
- call it to obtain time passed from last call

"""
from time import time


class Timer:
    """timer"""
    def __init__(self, threshold=-1.):
        self.t = time()
        self.threshold = threshold

    def __call__(self, print_='', show=True, precision=3):
        """call to take time from last call"""
        t = time()
        delta = t - self.t
        self.t = t
        if show:
            if delta > self.threshold:
                print(round(delta, precision), 's\t\t', print_)
        return delta


if __name__ == '__main__':

    from time import sleep

    timer = Timer()

    for I in range(-5, 0):
        sleep(10**I)
        timer()
