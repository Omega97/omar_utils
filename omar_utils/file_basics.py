"""
Basic operations with files
8/3/2019
"""
from os import makedirs, listdir, remove
from omar_utils.tensors import *
import shutil


def tab_to_file(path, data):
    """" save tensor in file """
    path = add_file_extension(path)
    file = open(path, 'w')
    file.write(tensor_to_string(data))
    file.close()


def file_split(path):
    """
    takes a file and splits it in a list of lists keeping strings together
    (removes blank lines)
    :param path: path to file
    :return: the split file
    """
    return [x.split() for x in read_file(path).split("\n") if x != '']


def file_to_list(path):
    """
    takes a file and splits it in a list of lists dividing strings
    (removes blank lines)
    :param path: path to file
    :return: the split file
    """
    return [x for x in read_file(path).split("\n") if x != '']


def add_file_extension(path):
    """ 'path' -> 'path.txt' """
    if len(path.split('.')) == 1:
        return path + '.txt'
    else:
        return path


def read_file(path):
    """ output file content as list """
    path = add_file_extension(path)
    try:
        file = open(path)
    except FileNotFoundError:
        print('File', path, 'not found')
        return
    return ''.join([i for i in file])


def write_file(path, text):
    """
    rewrite file
    :param path: path
    :param text: can be: 'aaa'; 111; ['aaa', 111]; [[1, 'dog'], [3]]
    """
    file = open(path, 'w')
    file.write(tensor_to_string(text))
    file.close()


def append_file(path, text):
    """
    append text to file
    :param path: path
    :param text: can be: 'aaa'; 111; ['aaa', 111]; [[1, 'dog'], [3]]
    """
    file = open(path, 'a+')
    file.write(tensor_to_string(text))
    file.close()


def file_to_tab(path, splitter=None):
    """ convert file to matrix """
    if splitter:
        v = [i.split(splitter) for i in file_to_list(path)]
    else:
        v = [i.split() for i in file_to_list(path)]

    for i in range(len(v)):
        if len(v[i]) == 1:
            if type(v[i][0]) == str:
                v[i] = [j for j in v[i][0]]
    w = []
    for i in v:
        if len(i) > 0:
            w += [i]
    return to_int(w)


# todo file to tensor?


def make_dir(path):
    """ create directory """
    try:
        makedirs(path)
    except FileExistsError:
        pass


def del_dir(path):
    """ delete directory """
    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass


def del_file(path):     # todo check
    """ delete file """
    path = add_file_extension(path)
    remove(path)


def list_files_in_dir(path):
    """ :returns list of files in path, None if path not found """
    try:
        return listdir(path)
    except FileNotFoundError:
        return


if __name__ == "__main__":
    ...

    from omar_utils.tensors import to_int

    V = [[i + 4 * j for i in range(4)] for j in range(3)]
    Path = 'test.txt'

    tab_to_file(Path, V)

    print(read_file(Path), '\n')
    print(file_to_list(Path), '\n')
    print(to_int(file_to_tab(Path)), '\n')

    del_file(Path)
