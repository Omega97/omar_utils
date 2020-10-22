"""     Sets


Intuitive Set class

- builtin set inheritance
- init a set using Set(a, b, c)
- sum sets with "+"
- use binary operations over two sets: & (AND), ^ (XOR), | (OR)
- iter over a Set
- also __eq__, __contains__

"""
__author__ = "Omar Cusma Fait"
__date__ = (19, 12, 2019)
__version__ = "2.0.0"

from copy import deepcopy


class Set(set):

    def __init__(self, *args):
        try:
            super().__init__(args)
        except TypeError:
            super().__init__(*args)

    def __add__(self, other):
        if type(other) in [set, Set]:
            s = deepcopy(self)
            s.update(other)
            return s
        else:
            return self

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return Set(set.__sub__(self, other))

    def __mul__(self, other):
        out = Set()
        for i in self:
            for j in other:
                out += Set(i * j)
        return out

    def apply(self, fun):
        """apply fun on each element of the set"""
        return Set([fun(i) for i in self])
