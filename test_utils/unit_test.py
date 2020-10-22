""" Simple unit test method"""
from copy import deepcopy


def unit_test(value, expected_output=None, validation_method=None, name='', do_report=True):
    """
    test whether dec method returns the correct value (or dec value accepted by validation_method)
    :param value: the value that you want to test
    :param expected_output: expected result     (if you know it)
    :param validation_method: True if value is plausible (not necessary if you know the expected_output)
    :param name: name of the value (to print in console in case something goes wrong)
    :param do_report: print report in the console in case something goes wrong
    :return: True if everything OK, else False
    """

    if validation_method is None:
        # validate using expected_output
        if value == expected_output:
            return True

        # print report if something goes wrong
        if do_report:
            print('\n', name, '\n\texpected: \t', expected_output, ' \n\treturned: \t', value)

    else:
        # validate using validation_method
        if validation_method(value):
            return True

        # print report if something goes wrong
        if do_report:
            print('\n', name, ' \n\treturned: \t', value)

    return False


def check(fun):
    """ check whether arguments of a function have been modified buy the function itself """
    def wrapper(*args):
        backup = deepcopy(args)
        out = fun(*args)
        if sum([not (args[j] == backup[j]) for j in range(len(args))]) > 0:
            print(fun.__name__, ': args have been modified! \t')
        return out
    return wrapper


def output_check(validation):
    """
    unit-testing decorator
    :param validation: validation function (output_) -> bool
    """
    def wrapper1(fun):
        def wrapper2(*args, **kwargs):
            out = fun(*args, **kwargs)
            if not validation(out):
                raise AssertionError('\n\n' + fun.__name__ + ' returned ' + str(out))
            return out
        return wrapper2
    return wrapper1


class Debug:

    count = 0

    def __call__(self, fun):
        def wrap(*args, **kwargs):
            s = f'{fun.__name__}('
            if len(args):
                s += f'{", ".join([str(i) for i in args])}'
            if len(kwargs):
                s += f', {", ".join([str(i) + "=" + str(kwargs[i]) for i in kwargs])}'
            s += ')'
            print('|\t' * (Debug.count))
            print('|\t' * Debug.count, s)
            Debug.count += 1
            out = fun(*args, **kwargs)
            s = f'{out}'
            Debug.count -= 1
            print('|\t' * (Debug.count + 1))
            print('|\t' * Debug.count, s)
            return out
        return wrap


# ------------------------------------------------------------------------


def __test_1():
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


def __test_2():

    @Debug()
    def f(a, x=1):
        return a + x

    @Debug()
    def g(b, y=2):
        return f(b) + y

    g(1)
    g(1, y=0)


if __name__ == "__main__":
    __test_2()
