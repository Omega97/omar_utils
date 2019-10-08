"""     Intuitive Set class

- built on builtin sets (fast!), so it behaves in a similar manner
- init a set using Set(a, b, c)
- easy to sum/subtract/multiply sets
- when summing remember to start from Set() !
- a Set automatically searches for double elements, if you are in a hurry then Set(..., fast=True) skips search
- use binary operations over two sets: & (AND), ^ (XOR), | (OR)
- iter over a Set
- also __eq__, __contains__
- cannot create a set of list, sets or unhashable elements
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.0.3"

from copy import deepcopy


class Set:
    """ Intuitive Set class """
    def __init__(self, *args):
        try:
            self.elements = {i for i in args}
        except TypeError:
            self.elements = {i for i in args[0]}

    def __call__(self, *args, **kwargs):
        return deepcopy(self.elements)

    def __repr__(self):
        return '{' + ', '.join([str(i) for i in self()]) + '}'

    def __len__(self):
        return len(self())

    def __iter__(self):
        return iter(self.elements)

    def __next__(self):
        return next(iter(self.elements))

    def __add__(self, other):
        if type(other) == Set:
            # join sets
            return Set(*self(), *other())
        elif type(other) == int or type(other) == float:
            # apply number to set
            return Set([i + other for i in self])
        else:
            # add into set
            return self + Set(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if type(other) == Set:
            # subtract set from set
            new = self()
            new.difference_update(other())
            return Set(new)
        elif type(other) == int or type(other) == float:
            # apply number to set
            return Set([i - other for i in self])
        else:
            # subtract element from set
            new = self()
            new.difference_update(other)
            return Set(new)

    def __mul__(self, other):
        if type(other) == Set:
            v = []
            for i in self:
                for j in other:
                    v += [i * j]
            return Set(v)
        elif type(other) == int or type(other) == float:
            # apply number to set
            return Set([i * other for i in self])

    def __contains__(self, item):
        return True if item in self.elements else False

    def intersect(self, other):
        return Set([i for i in self if i in other])

    def __eq__(self, other):
        return self() == other()

    def __and__(self, other):
        return self.intersect(other)

    def __xor__(self, other):
        return (self + other) - (self & other)

    def __or__(self, other):
        return self + other

    def apply(self, fun):
        """apply fun on each element of the set"""
        return Set([fun(i) for i in self])


if __name__ == '__main__':

    assert Set('a') + Set('b') == Set('a', 'b')
    assert Set('a', 'b') - Set('b') == Set('a')
    assert Set(1, 2) + Set(2, 3) == Set(1, 2, 3)
    assert Set(1, 2) - Set(2, 3) == Set(1)
    assert Set(1, 2) + 1 == Set(2, 3)
    assert Set(1, 2) - 1 == Set(0, 1)
    assert Set(1, 2) * 2 == Set(2, 4)
    assert Set('a', 'b') * Set(3, 2) == Set(['aa', 'aaa', 'bb', 'bbb'])
    assert Set(1, 2, 3) | Set(3, 4, 5) == Set([i+1 for i in range(5)])
    assert Set(1, 2, 3) & Set(3, 4, 5) == Set(3)
    assert Set(1, 2, 3) ^ Set(3, 4, 5) == Set(1, 2, 4, 5)
    assert Set(1, 2, 3).apply(lambda x: x+1) == Set(2, 3, 4)
    assert sum([Set(i+1) for i in range(5)]) == Set([i+1 for i in range(5)])
