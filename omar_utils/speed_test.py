""" How fast does Python run
26/2/2019
"""
from time import time
from statistics import mean, stdev


def speed_test(eta=10., tick=1., test_method=None):

    t0 = time()

    if not test_method:
        def test_method():
            """ used to slow down the test """
            for i in range(10**4):
                pass

    print('\n{:8s}{:8s}{:8s}\n'.format(' score', ' mean', ' st dev'))

    t = t0
    v = []
    count = 0
    epochs = 0

    while True:
        delta = time() - t

        # weight
        test_method()

        # tick
        count += 1
        if delta > tick:
            epochs += 1
            t = time()
            v.append(count)

            avg = mean(v)
            try:
                std = stdev(v)
            except:
                std = 0

            print('\n{:8d}{:8d}{:8d}'.format(count, round(avg), round(std)))

            count = 0
            if t-t0 > eta and epochs >= 1:
                break

    print('\n\nscore = %i (%i)\n' % (avg, std))
    print('\nmin = %i \t max = %i\n' % (min(v), max(v)))

    return v


if __name__ == "__main__":

    speed_test()
