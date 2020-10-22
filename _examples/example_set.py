from basic.Set import *


def example_1():
    a = Set('a', 'b')
    b = Set('a', 'c')
    print(a + b)
    print(a - b)


def example_2():
    """this is the case so you can do sum() of Set as well"""
    print(0 + Set('a'))
    print(sum(Set(i) for i in range(3)))


def example_3():
    print(Set('a', 'b') * Set(2, 3))


if __name__ == "__main__":
    example_1()
    example_2()
    example_3()
