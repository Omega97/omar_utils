""" Timer
- initialize a timer
- call it to take time passed from last call
- use .get_time() to get time lapsed
- use .total() to get total time
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.2.2"
__date__ = (22, 10, 2020)

from time import time


# ---------------------- time_decor ---------------------------


TIME_STORE = dict()


def time_decor(n=1):
    """decor a function to chronometer it (repeat call n times), show results with show_times()"""
    def _time_decor(fun):
        def __time_decor(*args, **kwargs):
            t = time()
            out = None
            for _ in range(n):
                out = fun(*args, **kwargs)
            t = (time() - t) / n
            if fun.__name__ not in TIME_STORE:
                TIME_STORE[fun.__name__] = {'list': []}
            TIME_STORE[fun.__name__]['list'] += [t]
            return out
        return __time_decor
    return _time_decor


def show_times(width=18, bar_len=24, n_digits=3):
    """display results of time_decor"""
    for i in TIME_STORE:
        TIME_STORE[i]['sum'] = sum(TIME_STORE[i]['list'])
        TIME_STORE[i]['avg'] = TIME_STORE[i]['sum'] / len(TIME_STORE[i]['list'])

    total_time = sum([TIME_STORE[i]['sum'] for i in TIME_STORE])
    for i in TIME_STORE:
        TIME_STORE[i]['norm'] = TIME_STORE[i]['sum'] / total_time if total_time else 0.

    print('_' * (width * 2 + width // 2 + bar_len + 8))
    print(f'\n{"NAME":>{width}}  '
          f'{"TOTAL":>{width // 2}}  '
          f'{"AVERAGE":>{width // 2}}  '
          f'{"N CALLS":>{width // 2}}  ')
    for i in TIME_STORE:
        print(f'{i:>{width}}  '
              f'{TIME_STORE[i]["sum"]:{width // 2}.{n_digits}f} s'
              f'{TIME_STORE[i]["avg"]:{width // 2}.{n_digits}f} s'
              f'{len(TIME_STORE[i]["list"]):{width // 2 + 2}}  '
              f'|{"=" * int(round(TIME_STORE[i]["norm"] * bar_len))}')
    print('\n', '_' * (width * 2 + width // 2 + bar_len + 8))


# ---------------------- Timer ---------------------------


class Timer:
    """ set "time" (in seconds), then
    return:
    True if called after "time" has passed,
    False otw.
    """
    def __init__(self, t=None):
        self.t0 = time()
        self.time = t

    def start(self, t=None):
        self.t0 = time()
        if t is not None:
            self.time = t

    def __call__(self, *args, **kwargs):
        assert self.time is not None
        t_ = time()
        return t_ - self.t0 >= self.time


class Clock:
    """set "time_period" (in seconds), then:
    return:
    True once after time_period has expired, then timer is reset
    False otw.
    """
    def __init__(self, time_period):
        self.t0 = time()
        self.last_t = self.t0
        self.time_period = time_period

    def start(self, time_period=None):
        self.t0 = time()
        if time_period is not None:
            self.time_period = time_period

    def __call__(self, *args, **kwargs):
        t_ = time()
        out = t_ - self.last_t >= self.time_period
        n = (t_ - self.t0) // self.time_period
        self.last_t = self.t0 + n * self.time_period
        return out


class Chronometer:
    """call to take time from last call"""
    def __init__(self):
        self.last_call = time()

    def __call__(self):
        """call to take time from last call"""
        t_ = time()
        out = t_ - self.last_call
        self.last_call = t_
        return out

    def __repr__(self):
        return f"{self():.3f} s"


class CumulativeChronometer:
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
