from test_utils.timer import *
from time import sleep


def __test_time_decor():

    @time_decor()
    def f():
        sleep(.15)

    @time_decor()
    def g():
        sleep(.2)

    f()
    g()
    g()

    show_times()


def __test_timer():
    timer = Timer(.5)
    for _ in range(3):
        timer.start(.15 * (_ + 1))
        sleep(.2)
        print(timer())
        sleep(.2)
        print(timer())
        sleep(.2)
        print(timer())
        print()


def __test_clock():
    clock = Clock(1.)
    t_ = 0
    dt = 0.15
    for _ in range(20):
        sleep(dt)
        t_ += dt
        if clock():
            print(round(t_, 2))


def __test_chronometer():
    chronometer = Chronometer()
    sleep(.1)
    print(chronometer())
    sleep(.2)
    print(chronometer())


def __test_cumulative_timers():

    t = CumulativeChronometer(dec=3)

    t.start('a')    # init timer 'a'
    sleep(.1)
    t.stop('a')

    t('d')
    sleep(.1)

    for I in range(5):

        t('b')  # like T.start('b')
        sleep(.01)
        t.stop('b')     # stop timer 'b'

        t('c')
        sleep(.02)
        t.stop()    # stopping timer 'd'

    t.stop_all()    # stopping all timers

    print(t)
    print(t['a'])


if __name__ == '__main__':
    __test_timer()
    __test_clock()
    __test_chronometer()
    __test_cumulative_timers()
    __test_time_decor()
