"""
                        Iter

This simple object allows for a fast and clean creation
and visualization of the data pipeline inside a generator

1) create the Iter object out of an iterable
2) modify it by applying functions

"""


class Iter:

    def __init__(self, item):
        if not hasattr(item, '__iter__'):
            raise TypeError('item is not iterable')
        self.item = item

    def __iter__(self):
        return iter(self.item)

    def __or__(self, other):
        return Iter(other(self))
