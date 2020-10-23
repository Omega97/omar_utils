from basic.decorators import *


def example_avg_time():

    @take_average_time(10)
    def list_range(n):
        return list(range(n))

    @take_average_time(10)
    def list_comprehension(n):
        return [i for i in range(n)]

    num = 10 ** 5
    t1 = list_range(num)
    t2 = list_comprehension(num)

    for t in [t1, t2]:
        print(f'{t * 1000:.1f} ms')


if __name__ == '__main__':
    example_avg_time()
