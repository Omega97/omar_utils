""" How fast does Python run

Keep in mind that this is a relative score, makes sense only if compared to other PCs
"""
from time import time
from statistics import mean, stdev, StatisticsError


def speed_test(eta=6., tick=1., test_method=None):
    """ how fast does Python run """
    t0 = time()

    if not test_method:
        def test_method():
            """ used to slow down the test """
            for i in range(10**4):
                pass

    print('\n\nSpeed test\n')

    print('\n\t{:8s}{:8s}{:8s}\n'.format('score', 'mean', 'st dev'))

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
            except StatisticsError:
                std = 0

            print('\n\t{:8s}{:8s}{:8s}'.format(str(count), str(round(avg)), str(round(std))))

            count = 0
            if t-t0 > eta and epochs >= 1:
                break

    print('\n' * 3 + 'SCORE = %i (%i)\n' % (avg, std))
    print('\nmin = %i \t max = %i\n' % (min(v), max(v)))

    return v


if __name__ == "__main__":
    speed_test()
