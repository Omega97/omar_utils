from basic.Set import *


def test_1():
    assert Set('a') + Set('b') == Set('a', 'b')
    assert Set('a', 'b') - Set('b') == Set('a')
    assert Set(1, 2) + Set(2, 3) == Set(1, 2, 3)
    assert Set(1, 2) - Set(2, 3) == Set(1)
    assert Set(1, 2, 3) | Set(3, 4, 5) == Set([i + 1 for i in range(5)])
    assert Set(1, 2, 3) & Set(3, 4, 5) == Set(3)
    assert Set(1, 2, 3) ^ Set(3, 4, 5) == Set(1, 2, 4, 5)
    assert Set(1, 2, 3).apply(lambda x: x + 1) == Set(2, 3, 4)
    assert Set('a', 'b') * Set(3, 2) == Set(['aa', 'aaa', 'bb', 'bbb'])
    assert sum([Set(i + 1) for i in range(5)]) == Set([i + 1 for i in range(5)])
    assert sum([Set(1), Set(2)]) == Set(1, 2)
    assert 0 + Set(1) == Set(1)


if __name__ == '__main__':
    test_1()
