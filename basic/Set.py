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
        if type(other) == set or type(other) == Set:
            s = deepcopy(self)
            s.update(other)
            return s
        else:
            return self

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        out = Set()
        for i in self:
            for j in other:
                out += Set(i * j)
        return out

    def apply(self, fun):
        """apply fun on each element of the set"""
        return Set([fun(i) for i in self])


if __name__ == '__main__':

    assert Set('a') + Set('b') == Set('a', 'b')
    assert Set('a', 'b') - Set('b') == Set('a')
    assert Set(1, 2) + Set(2, 3) == Set(1, 2, 3)
    assert Set(1, 2) - Set(2, 3) == Set(1)
    assert Set(1, 2, 3) | Set(3, 4, 5) == Set([i+1 for i in range(5)])
    assert Set(1, 2, 3) & Set(3, 4, 5) == Set(3)
    assert Set(1, 2, 3) ^ Set(3, 4, 5) == Set(1, 2, 4, 5)
    assert Set(1, 2, 3).apply(lambda x: x+1) == Set(2, 3, 4)
    assert Set('a', 'b') * Set(3, 2) == Set(['aa', 'aaa', 'bb', 'bbb'])
    assert sum([Set(i+1) for i in range(5)]) == Set([i+1 for i in range(5)])
