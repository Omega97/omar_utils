""" simple unit test method

"""


def test_unit(value, expected_output=None, validation_method=None, name='', do_report=True):
    """
    tend whether a method returns the correct value (or a value accepted by validation_method)
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


if __name__ == "__main__":

    # TEST 1

    def f(x):
        return x

    test_unit(f(0), expected_output=0, name='f')
    test_unit(f(1), expected_output=0, name='f')
    test_unit(f(1), expected_output='dog???', name='f')

    # TEST 2

    def g(x):
        return x / 2

    def valid(x):
        return int(x) == x

    for i in range(-2, 3):
        test_unit(g(i), validation_method=valid, name='g')

    # TEST 3

    n = 1.

    def valid(x):
        a = x / 2
        return 2 * a == x

    while test_unit(n, validation_method=valid):
        n /= 2
