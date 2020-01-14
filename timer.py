""" Timer
- initialize a timer
- call it to take time passed from last call
- use .get_time() to get time lapsed
- use .total() to get total time
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.0.2"

from time import time, sleep


# -------------------------------- Timer --------------------------------


class Timer:
    """timer: call to take time from last call (or from initialization)"""
    def __init__(self):
        self.last_call = time()     # time of last call
        self.t = None   # time lapsed from last call

    def __repr__(self):
        self()
        return f"{self.get_time():.3f} s"

    def _take_time(self):
        """takes time and computes lapse"""
        t = time()
        self.t = t - self.last_call
        self.last_call = t

    def get_time(self):
        return self.t

    def __call__(self):
        """call to take time from last call"""
        self._take_time()
        return self.get_time()


# -------------------------------- CumulativeTimers --------------------------------


class CumulativeTimers:
    """multiple timers in one class
    start(name) to start a timer with that name
    stop(name) to stop the timer
    print() to show every timer
    time gets added from start to stop
    """

    def __init__(self, dec=4):
        self.timers = dict()
        self.name = None
        self.dec = dec

    def __getitem__(self, item):
        try:
            return self.timers[item]
        except KeyError:
            error = True
        if error:
            c = '"'
            raise(KeyError(f"use start({c}{self.name}{c}) to start the timer before stopping it"))

    def __repr__(self):
        tot = self.total()

        def line(name):
            p = self[name]["t"]/tot
            return f'{name} \t {self[name]["t"]:.{self.dec}f} s \t {p*100:.1f}% \t |{"=" * round(p*40)}'

        return '\n' + '\n'.join(line(name) for name in self.timers) + '\n'

    def _add_timer(self, name):
        if name not in self.timers:
            self.timers.update({self.name: {'t': 0.}})

    def _update_current_name(self, name):
        if name:
            self.name = name

    def _current_timer(self):
        return self[self.name]

    def _take_time(self, name):
        t0 = self[name]['last call']
        if name and t0:
            self[name]['t'] += time() - t0
        self[name].pop('last call')

    def start(self, name=None):
        self._update_current_name(name)
        self._add_timer(self.name)
        self._current_timer()['last call'] = time()

    def stop(self, name=None):
        """terminates current measure, adds t to the last timer"""
        self._update_current_name(name)
        self._take_time(self.name)

    def total(self):
        return sum(self[i]['t'] for i in self.timers)


# -------------------------------- TIMERS --------------------------------


def _test_timer():

    timer = Timer()

    sleep(.1)
    print(timer)    # print object

    sleep(.15)
    print(timer())  # print float value


def _test_cumulative_timers():

    T = CumulativeTimers(dec=3)

    T.start('a')

    for I in range(5):

        T.start('b')
        sleep(.01)
        T.stop('b')

        T.start('c')
        sleep(.05)
        T.stop('c')

    sleep(.15)
    T.stop('a')

    T.start('d')
    sleep(.2)
    T.stop('d')

    print(T)
    print(T['a'])


if __name__ == '__main__':
    _test_timer()
    _test_cumulative_timers()
