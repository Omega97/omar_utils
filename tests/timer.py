""" Timer

Timer class

- initialize a timer
- call it to take time passed from last call
- use .get_time() to get time lapsed
- use .total() to get total time


CumulativeTimers

track multiple methods at the same time


CumulativeTimers.decorator

Inside a class MyClass, write:
timer = CumulativeTimers()

Decore your methods with:
@timer.decorator()

At the end, display results
print(MyClass.timer)
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.1.0"
__date__ = (12, 3, 2020)

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

    def __init__(self, dec=2):
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

        if not tot:
            return 'No data to display'

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

    def decorator(self):
        """
        Inside a class MyClass, write:
        timer = CumulativeTimers()

        Decore your methods with:
        @timer.decorator()

        At the end, display results
        print(MyClass.timer)
        """
        def wrap(fun):
            def wrap2(*args, **kwargs):
                name = fun.__name__
                self.start(name)
                out = fun(*args, **kwargs)
                self.stop(name)
                return out
            return wrap2
        return wrap


# -------------------------------- TIMERS --------------------------------


def _test_timer():

    timer = Timer()

    for I in range(-11, -2):
        # do stuff...
        sleep(2**I)
        # call to take time & print
        timer()
        # use get_time to obtain time lapsed from last call
        if timer.get_time() < .01:
            print('fast!')
        else:
            print('not so fast!')


def _test_cumulative_timers():

    T = CumulativeTimers(dec=3)

    T.start('a')

    for I in range(3):

        T.start('b')
        sleep(.1)
        T.stop('b')

        T.start('c')
        sleep(.05)
        T.stop('c')


    sleep(.15)
    T.stop('a')

    T.start('d')
    sleep(.6)
    T.stop('d')

    print(T)
    print(T['a'])


def _test_cumulative_timers_decorator():

    class Class:
        timer = CumulativeTimers()

        @timer.decorator()
        def foo(self):
            sleep(.2)

        @timer.decorator()
        def bar(self):
            sleep(.3)

    c = Class()
    c.foo()
    c.bar()

    print(Class.timer)


if __name__ == '__main__':
    _test_timer()
    _test_cumulative_timers()
    _test_cumulative_timers_decorator()
