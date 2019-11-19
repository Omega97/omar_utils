""" Timer
- initialize a timer
- call it to take time passed from last call
- use .get_time() to get time lapsed
- use .total() to get total time
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.0.2"

from time import time


class Timer:
    """timer"""
    def __init__(self, tag='', precision=3):
        self.t = time()
        self.tot_t = 0
        self.lapse = None
        self.precision = precision
        self.tag = tag

    def __repr__(self):
        return f"\t[  {self.get_time():.{str(self.precision)}f} s  ] \t {self.tag}"

    def take_time(self):
        """takes time and computes lapse"""
        t = time()
        self.lapse = t - self.t
        self.tot_t += self.lapse
        self.t = t

    def get_time(self):
        """:returns time lapsed from last call"""
        return self.lapse

    def total(self, tag='TOT'):
        timer_ = Timer()
        timer_.lapse = self.tot_t
        timer_.tag = tag
        return self.tot_t

    def __call__(self, tag=None):
        """call to take time from last call"""
        if tag is not None:
            self.tag = str(tag)
        self.take_time()
        return self


if __name__ == '__main__':

    from time import sleep

    timer = Timer()

    for I in range(-11, -1):
        # do stuff...
        sleep(2**I)
        # call to take time & print
        print(timer(tag=I))
        # use get_time to obtain time lapsed from last call
        if timer.get_time() < .01:
            print('fast!')

    timer.total()
