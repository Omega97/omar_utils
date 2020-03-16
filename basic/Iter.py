"""stackable iterators"""
from omar_utils import q_print


class Iter:
    def __init__(self, item):
        """
        :param item: generator or function
        """
        self.item = item

    def __iter__(self):
        return self.item

    def __or__(self, other):
        return other.item(self.item)

    def __ror__(self, other):
        return Iter(self.item(other))


def gen_next_n(n) -> Iter:
    def f(itr, m=n):
        """generator of next n items when called"""
        for i in itr:
            m -= 1
            if m < 0:
                break
            yield i
    return Iter(f)


def one_in_n(n) -> Iter:
    def f(itr):
        """yields only one element every n"""
        j = n
        for i in itr:
            j -= 1
            if not j:
                yield i
                j = n
    return Iter(f)


def filter_iter(criterion) -> Iter:
    def f(itr):
        """yields only elements of itr that match the criterion"""
        for i in itr:
            if criterion(i):
                yield i
    return Iter(f)


# ------------------------------------------------------------


def __test_0():
    """ iterable -> Iter """
    I = Iter(iter)  # Identity
    a = range(5) | I
    q_print(a)


def __test_1(n_next=6, n_freq=2, n_mod=3):
    def gen():
        n = 0
        while True:
            yield n
            n += 1

    crit = lambda x: x % n_mod == 0

    a = gen() | one_in_n(n_freq) | filter_iter(crit) | gen_next_n(n_next)
    q_print(a)

    a = gen() | filter_iter(crit) | one_in_n(n_freq) | gen_next_n(n_next)
    q_print(a)

    a = gen() | filter_iter(crit) | gen_next_n(n_next) | one_in_n(n_freq)
    q_print(a)


if __name__ == '__main__':
    __test_0()
    __test_1()
