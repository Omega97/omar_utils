""" Timer
- initialize a timer
- call it to take time passed from last call
- use .get_time() to get time lapsed
- use .total() to get total time
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.0.3"
__date__ = (14, 1, 2020)

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
    the time between start() to stop() gets added to the timer
    """

    def __init__(self, dec=4):
        self.timers = dict()        # dict of {name: time}, describes time from start to stop
        self.last_calls = dict()    # time of last call of each timer
        self.dec = dec              # decimal digits
        self.last_name = None       # last timer name used, avoids writing names every time

    def __getitem__(self, item):
        try:
            return self.timers[item]
        except KeyError:
            error = True
        if error:
            raise(KeyError(f"timer {item} not found!"))

    def __setitem__(self, key, value):
        self.timers[key] = value

    def __iter__(self):
        """iter through timer names"""
        return iter(self.timers)

    def __repr__(self):
        tot = self.total()

        def line(name):
            p = self[name] / tot
            return f'{name:<16}' \
                   f'{self[name]:.{self.dec}f} s \t' \
                   f'{p*100:.1f}% \t' \
                   f'|{"=" * round(p*40)}'

        out = '\n' + '_' * 80 + '\n'
        out += '\n'.join(line(name) for name in self.timers)
        out += '\n' + '-' * 80 + '\n'
        out += ' ' * 16 + f'{self.total():.{self.dec}f} s'
        out += '\n' + '_' * 80 + '\n'

        return out

    def _check_name(self, name):
        return self.last_name if name is None else name

    def _add_timer(self, name):
        if name not in self.timers:
            self.timers.update({name: 0.})

    def start(self, name=None):
        name = self._check_name(name)
        self.last_name = name
        self._add_timer(name)
        self.last_calls[name] = time()

    def __call__(self, name=None):
        name = self._check_name(name)
        self.start(name)

    def stop(self, name=None):
        """terminates current measure, adds t to the last timer"""
        name = self._check_name(name)
        t0 = self.last_calls[name]
        if name and t0:
            self[name] += time() - t0

    def stop_all(self):
        """stop all timers"""
        for i in self:
            self.stop(i)

    def total(self):
        """total time of all timers"""
        return sum(self[i] for i in self.timers)

    def get_timers(self):
        return self.timers


# -------------------------------- TIMERS --------------------------------


def _test_timer():

    timer = Timer()

    sleep(.1)
    print(timer)    # print object

    sleep(.15)
    print(timer())  # print float value


def _test_cumulative_timers():

    T = CumulativeTimers(dec=3)

    T.start('a')    # init timer 'a'
    sleep(.1)
    T.stop('a')

    T('d')
    sleep(.1)

    for I in range(5):

        T('b')  # like T.start('b')
        sleep(.01)
        T.stop('b')     # stop timer 'b'

        T('c')
        sleep(.02)
        T.stop()    # stopping timer 'd'

    T.stop_all()    # stopping all timers

    print(T)
    print(T['a'])


if __name__ == '__main__':
    _test_timer()
    _test_cumulative_timers()
