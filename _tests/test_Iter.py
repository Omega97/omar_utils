from basic.Iter import *
from basic.iter_utils import *


def test_0():
    """
    1) create the Iter object out of an iterable
    2) modify it by applying functions with the | symbol
    """
    a = Iter(range(5)) | one_in_n(2)
    i_print(a)


def test_1(n_next=6, n_freq=2, n_mod=3):
    """try applying the mods in different order"""
    gen = Iter(infinite_range())

    def rule(x):
        return x % n_mod == 0

    i_print(gen | one_in_n(n_freq) | filter_iter(rule) | gen_next_n(n_next))
    i_print(gen | filter_iter(rule) | one_in_n(n_freq) | gen_next_n(n_next))
    i_print(gen | filter_iter(rule) | gen_next_n(n_next) | one_in_n(n_freq))


if __name__ == '__main__':
    test_0()
    test_1()
