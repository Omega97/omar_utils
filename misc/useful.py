"""         Useful
Collection of useful 'implement once' methods
"""
__author__ = "Omar Cusma Fait"
__date__ = (16, 12, 2019)
__version__ = '1.0.1'


def describe(item, starts_with=None, has_in_name=None):
    """print all attributes of item and more"""
    print(f'\n{type(item).__name__} object\n')
    for name in dir(item):
        do_print = True
        if starts_with:
            if not name[:len(starts_with)] == starts_with:
                do_print = False
        if has_in_name:
            if has_in_name not in name:
                do_print = False
        if do_print:
            print(name)
    return dir(item)


def nested_print(x, depth=-1):
    """print with indentation, more nested = more indentation"""
    if hasattr(x, '__iter__') and type(x) != str:
        for i in x:
            nested_print(i, depth=depth+1)
    else:
        print('\t' * depth, end='')
        print(x)


class Default:
    """
    D = Default
    x |D (default)  <<< returns x if x is not None, else  returns default
    """
    def __init__(self, value):
        self.value = value

    def __ror__(self, other):
        return self.value if other is None else other
