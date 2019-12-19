"""         Dict

- inheritance from dict
- join dicts with "+"
- remove keys with "-"

"""
__author__ = "Omar Cusma Fait"
__date__ = (19, 12, 2019)
__version__ = "1.0.0"

from copy import deepcopy


class Dict(dict):

    def __add__(self, other):
        """join dicts (multiple values for keyword argument NOT allowed)"""
        return Dict(**self, **other)

    def __sub__(self, other):
        """:return Dict with keys from self but without keys of other"""
        d = deepcopy(self)
        for i in other.keys():
            d.pop(i)
        return d


if __name__ == '__main__':

    a = Dict(a=1)
    b = Dict(a=2, b=2)

    print(b - a)
    print(a)
    print(b)
