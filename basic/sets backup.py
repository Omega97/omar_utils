"""     Intuitive Set class

- init a set using Set(a, b, c) or Set(*[a, b, c]) (to indicate that the array contains the arguments)
- easy to sum/subtract/multiply sets
- when summing remember to start from Set() !
- a Set automatically searches for double elements, if you are in a hurry then Set(..., fast=True) skips search
- can be sorted even if contains strings or lists
- use binary operations over two sets: & (AND), ^ (XOR), | (OR)
- iter over a Set
- sort with .sort() or create a sorted copy with .sorted()
- set items and get items
- also __eq__, __contains__
"""
__author__ = "Omar Cusma Fait"
__version__ = "1.0.1"

from copy import deepcopy


class Set:
    """
    Intuitive Set class
    note: args must have __repr__ in order to be sortable
    """
    def __init__(self, *args, fast=False):
        """
        :param args: elements of the Set, if you want to use a list of args, then do Set(*[...])
        :param fast: if True, skips checking for double elements, faster
        """
        self.elements = [i for i in args]
        self.index = 0
        if not fast:
            self.simplify()

    def __call__(self, *args, **kwargs):
        return deepcopy(self.elements)

    def __repr__(self):
        return '{' + ', '.join([str(i) for i in self.sorted()()]) + '}'

    def __len__(self):
        return len(self())

    def __getitem__(self, item):
        return self()[item]

    def __setitem__(self, key, value):
        self.elements[key] = value

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self):
            self.index = 0
            raise StopIteration
        out = self[self.index]
        self.index += 1
        return out

    def __add__(self, other):
        if type(other) == Set:
            return Set(*self(), *other())
        else:
            return self + Set(other)

    def __radd__(self, other):
        return self + other     # +other? bugs with sum()

    def __sub__(self, other):
        if type(other) == Set:
            return Set(*[i for i in self() if i not in other()], fast=True)
        else:
            return self - Set(other)

    def __mul__(self, other):
        if type(other) == Set:
            v = []
            for i in self:
                for j in other:
                    v += [i * j]
            return Set(*v)

    def __contains__(self, item):
        return True if item in self.elements else False

    def simplify(self):
        """delete redundant elements"""
        v = []
        for i in self():
            if i not in v:
                v.append(i)
        self.elements = v

    def sorted(self, reverse=False):
        """:returns the sorted version of self"""
        def key(x):
            if type(x) == int or type(x) == float:
                return x
            else:
                s = str(x)
                return sum([ord(s[i]) * 256**i for i in range(len(s))])
        try:
            return Set(*sorted(self(), reverse=reverse), fast=True)
        except TypeError:
            return Set(*sorted(self(), reverse=reverse, key=key), fast=True)

    def sort(self):
        self.elements = self.sorted()()

    def intersect(self, other):
        return Set(*[i for i in self if i in other], fast=True)

    def __eq__(self, other):
        self.sort()
        other.sort()
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
