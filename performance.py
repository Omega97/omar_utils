from time import time


class Performance:
    data = dict()
    first_call = None
    last_call = None

    def __call__(self, fun):

        def wrap(*args, **kwargs):
            t = time()
            if Performance.first_call is None:
                Performance.first_call = t
            out = fun(*args, **kwargs)
            t = time() - t
            if fun.__name__ not in Performance.data:
                Performance.data[fun.__name__] = {'time': t, 'n': 1}
            else:
                Performance.data[fun.__name__]['time'] += t
                Performance.data[fun.__name__]['n'] += 1
            Performance.last_call = time()
            return out

        return wrap


def print_performance(width=12, tot_digits=2, avg_digits=4):
    data = Performance.data
    if not data:
        print('\nNothing to show!')
        return
    print(f'\n {"name":<{width * 2}}{"count":<{width}}{"avg":<{width}}{"total":<{width}}{"proportion":<{width}}')
    tot_time = Performance.last_call - Performance.first_call
    for key in data:
        t = data[key]['time']
        n = data[key]['n']
        p = f'{t / tot_time * 100:<.1f}%'
        print(f' {key:<{width*2}}{n:<{width}}{t/n:<{width}.{avg_digits}f}{t:<{width}.{tot_digits}f}{p:<{width}}')


def get_time(method, min_time=10**-3, min_n_repeat=1):
    t0 = time()
    n = 1
    while True:
        method()
        t = time() - t0
        if t > min_time and n >= min_n_repeat:
            return t / n
        n += 1
