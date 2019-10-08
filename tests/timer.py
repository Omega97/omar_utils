""" Timer

- initialize a timer
- call it to take time passed from last call
- use .get_time to get time lapsed
"""
from time import time


class Timer:
    """timer"""
    def __init__(self, tag='', precision=3):
        self.t = time()
        self.lapse = None
        self.precision = precision
        self.tag = tag

    def __repr__(self):
        return f"[  {self.get_time():.{str(self.precision)}f} s  ] \t {self.tag}"

    def take_time(self):
        """takes time and computes lapse"""
        t = time()
        self.lapse = t - self.t
        self.t = t

    def get_time(self):
        """:returns time lapsed from last call"""
        return self.lapse

    def __call__(self, tag=None):
        """call to take time from last call"""
        if tag is not None:
            self.tag = str(tag)
        self.take_time()
        return self


if __name__ == '__main__':

    from time import sleep

    timer = Timer(precision=3)

    for I in range(-11, -1):
        # do stuff...
        sleep(2**I)
        # get time & print
        print(timer(tag=I))
        # use time (lapsed from last call)
        if timer.get_time() > .1:
            print('slow!')
