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
    """timer: call to take time from last call (first time from init)"""
    def __init__(self, tag='', precision=3, show=True):
        self.t = time()
        self.tot_t = 0
        self.lapse = None
        self.precision = precision
        self.show = show
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
        if self.show:
            print(timer_)
        return self.tot_t

    def __call__(self, tag=None):
        """call to take time from last call"""
        if tag is not None:
            self.tag = str(tag)
        self.take_time()
        if self.show:
            print(self)
        return self


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

    for I in range(-11, -1):
        # do stuff...
        sleep(2**I)
        # call to take time & print
        timer(tag=I)
        # use get_time to obtain time lapsed from last call
        if timer.get_time() < .01:
            print('fast!')

    timer.total()


def _test_cumulative_timers():

    T = CumulativeTimers(dec=4)

    T.start('a')

    for I in range(3):

        T.start('b')
        sleep(.1)
        T.stop('b')

    sleep(.15)
    T.stop('a')

    T.start('c')
    sleep(.6)
    T.stop('c')

    print(T)
    print(T['a'])


if __name__ == '__main__':
    _test_timer()
    _test_cumulative_timers()
