from misc.useful import *


def example_default_1():
    """when Default sees a None it overwrites it with the specified value"""
    print(None | Default('default'))


def example_default_2():
    """when Default sees a None it overwrites it with the specified value"""
    print('not default' | Default('default'))


def example_describe():
    """show all there is to know about some object"""
    describe(list, starts_with='_', has_in_name='l')


if __name__ == '__main__':
    # example_default_1()
    # example_default_2()
    example_describe()
