from test_utils.unit_test import *


def test_1():
    @check
    def f(x):
        return x

    unit_test(f(0), expected_output=0, name='ex 1')
    unit_test(f(1), expected_output=0, name='ex 2')
    unit_test(f(1), expected_output='dog???', name='ex 3')

    def valid(out) -> bool:
        return int(out) == out

    @output_check(valid)
    def f(x):
        return x

    f(1)


def test_2():

    @Debug()
    def f(a, x=1):
        return a + x

    @Debug()
    def g(b, y=2):
        return f(b) + y

    g(1)
    g(1, y=0)


if __name__ == "__main__":
    test_1()
    test_2()
