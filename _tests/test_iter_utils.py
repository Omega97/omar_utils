from basic.iter_utils import *


def test_frequently_used():
    a = infinite_range()
    a = skip_n(2)(a)
    a = one_in_n(4)(a)
    assert list(gen_next_n(4)(a)) == [2, 6, 10, 14]
    assert list(gen_next_n(2)(a)) == [18, 22]
    assert list(group_by_n(2)(range(4))) == [(0, 1), (2, 3)]


def test_files():
    name = '_test_file.txt'
    with open(name, 'w') as file:
        file.write('1\n2\n\n3\n4\n')

    i_print(read_file(name))
    i_print(read_file_lines(name))

    os.remove(name)


def test_str(*args, n=20):

    v = [1, 2, 0, 3, 4, 0]
    gen = group_by(lambda x: x == 0)(v)
    i_print(gen)

    gen = (str(i) for i in range(n))
    gen = skip_starts_with(*args)(gen)
    i_print(gen)

    gen = (str(i) for i in range(n))
    gen = keep_starts_with(*args)(gen)
    i_print(gen)

    gen = (str(i) for i in range(n))
    gen = skip_ends_with(*args)(gen)
    i_print(gen)

    gen = (str(i) for i in range(n))
    gen = keep_ends_with(*args)(gen)
    i_print(gen)


def test_less_used():
    v = [4, 4, 4, 5, 5, 6]
    gen = count_gen(v)
    gen = gen_apply(lambda x: str(d_print(x)))(gen)
    list(gen)


def test_time():
    gen = yield_timer(.5)
    gen = gen_next_n(6)(gen)
    for i in gen:
        print(i)


def test_special():
    i_print(recursive_iter(['a', 'b'], range(3), range(1, 4)))
    gen = range(30)
    gen = split_data(1/3)(gen)
    i_print(gen)


def test_decorators():
    @gen_next_n_decorator(5)    # gen now yields only 5 elements
    def gen():
        return infinite_range()
    i_print(gen())




if __name__ == '__main__':
    test_frequently_used()
    test_files()
    test_str('1', '2', '3')
    test_less_used()
    test_time()
    test_special()
    test_decorators()
