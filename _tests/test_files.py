from basic.files import *


def __test():
    name = 'data.txt'

    write_file(name, 'a b c\n1 2 3')
    append_file(name, 'new')
    data = file_to_list(name)
    assert data == ['a b c', '1 2 3', 'new']
    assert file_to_tab(name) == [['a', 'b', 'c'], [1, 2, 3], ['new']]
    del_file(name)

    tab = [[1, '2'], ['c', 'D']]
    tab_to_file(name, tab)
    assert file_to_tab(name) == [[1, 2], ['c', 'D']]
    del_file(name)

    text = '古'
    write_file(name, text)
    assert read_file(name) == '古'
    assert type(read_file(name)) == str
    del_file(name)


if __name__ == "__main__":
    __test()
