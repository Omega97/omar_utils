"""     Intuitive Set class

- init a set using Set(a, b, c) or Set(*[a, b, c]) (to indicate that the array contains the arguments)
- easy to sum/subtract/multiply sets
- when summing remember to start from Set() !
- a Set automatically searches for double elements, if you are in a hurry then Set(..., fast=True) skips search
- use binary operations over two sets: & (AND), ^ (XOR), | (OR)
- iter over a Set
- also __eq__, __contains__
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.0.2"

from copy import deepcopy


class Set:
    """ Intuitive Set class """
    def __init__(self, *args):
        """
        :param args: elements of the Set, if you want to use a list of args, then do Set(*[...])
        """
        self.elements = {i for i in args}

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
            return Set(*self(), *other())
        else:
            return self + Set(other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if type(other) == Set:
            new = self()
            new.difference_update(other())
            return Set(*new)
        else:
            new = self()
            new.difference_update(other)
            return Set(*new)

    def __mul__(self, other):
        if type(other) == Set:
            v = []
            for i in self:
                for j in other:
                    v += [i * j]
            return Set(*v)

    def __contains__(self, item):
        return True if item in self.elements else False

    def intersect(self, other):
        return Set(*[i for i in self if i in other])

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
        return Set(*[fun(i) for i in self])


if __name__ == '__main__':

    assert Set() + 'e' == Set('e')
    assert 'e' + Set() == Set('e')
    assert Set('e') - 'e' == Set()
    assert Set(1, 2) + Set(2, 3) == Set(1, 2, 3)
    assert Set(1, 2) - Set(2, 3) == Set(1)
    assert Set('a', 'b') * Set(3, 2) == Set(*['aa', 'aaa', 'bb', 'bbb'])
    assert Set(1, 2, 3) | Set(3, 4, 5) == Set(*[i+1 for i in range(5)])
    assert Set(1, 2, 3) & Set(3, 4, 5) == Set(3)
    assert Set(1, 2, 3) ^ Set(3, 4, 5) == Set(1, 2, 4, 5)
    assert Set(1, 2, 3).apply(lambda x: x+1) == Set(2, 3, 4)
    assert sum([Set(i+1) for i in range(10)], Set()) == Set(*[i+1 for i in range(10)])
