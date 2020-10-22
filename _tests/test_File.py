from data.File import *
from os import remove


def _test_1(path='data.pkl'):
    """download & save & load_file"""
    print('\n\n\t TEST 1 \n')
    url = 'https://raw.githubusercontent.com/Omega97/google_hash/master/example/problems/a_example.txt'
    f = File(url=url, path=path)
    print(f().head())
    remove(path)


if __name__ == '__main__':
    _test_1()
