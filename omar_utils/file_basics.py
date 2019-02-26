""" Basic operations with files
26/2/2019
"""
from os import makedirs, listdir, remove
from omar_utils.tensors import apply_to_tensor, tensor_to_string
import shutil


def read_file(path):
    """ output file content as list """
    if len(path.split('.')) == 1:
        path += '.txt'
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


def file_to_tab(name, convert_to=None):     # todo tensor?
    """ convert file to str matrix """
    if len(name.split('.')) == 1:
        name += '.txt'
    try:
        file = open(name)
    except FileNotFoundError:
        print('File', name, 'not found')
        return
    m = [[j for j in i.split()] for i in file]
    if convert_to:
        return apply_to_tensor(m, convert_to)
    else:
        return m


def tab_to_file(name, data):
    """" save tensor in file """
    if len(name.split('.')) == 1:
        name += '.txt'
    file = open(name, 'w')
    file.write(tensor_to_string(data))
    file.close()


def file_to_list(path):
    """ output file content as str """
    return read_file(path).split('\n')


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


def del_file(path):     # todo
    """"""
    if len(path.split('.')) == 1:
        path += '.txt'
    remove(path)


def list_files_in_dir(path):
    """ :returns list of files in path, None if path not found """
    try:
        return listdir(path)
    except FileNotFoundError:
        return


if __name__ == "__main__":
    ...
