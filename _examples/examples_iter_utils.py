from basic.iter_utils import *


def example_1():
    v = [1, 2, 'a', 3, 4, 'b', 5, -2, 'c']
    gen = group_by_n(3)(v)
    gen = gen_apply(lambda x: x[0] + x[1])(gen)
    gen = count_gen(gen)
    i_print(gen)


if __name__ == '__main__':
    example_1()
