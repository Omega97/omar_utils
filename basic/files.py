"""         Files

Basic operations with files

save obj
"""
__author__ = "Omar Cusma Fait"
__date__ = (5, 4, 2021)
__version__ = '1.1.0'

import os
import pickle

if __name__ == '__main__':
    from basic.tensors import *
else:
    from ..basic.tensors import *


def write_file(path, text, encoding='utf-8'):
    """rewrite file"""
    with open(path, "w", encoding=encoding) as file:
        file.write(text)


def read_file(path, encoding='utf-8') -> str:
    """output file content as list"""
    with open(path, encoding=encoding) as file:
        return file.read()


def append_file(path, text, new_line='\n'):
    """append text to file"""
    with open(path, 'a') as file:
        file.write(new_line + text)


def paths_in_dir(path):
    """generator of all paths in path"""
    for name in os.listdir(path):
        yield path + '\\' + name


def count_files(path):
    """count the number of files in a directory"""
    path = path.replace('"', '')
    if not os.path.isdir(path):
        return True
    else:
        return sum(count_files(i) for i in paths_in_dir(path))


def file_to_list(path):
    """takes dec file and splits it in dec list of lists dividing strings (removes blank lines)"""
    v = [x for x in read_file(path).split('\n') if x != '']
    return apply_to_tensor(v, soft_to_float)


def list_to_file(path, v):
    """list -> file"""
    write_file(path, '\n'.join(apply_to_tensor(v, str)))


def tab_to_file(path, data, separator='\t'):
    """" save tensor in file """
    with open(path, 'w') as file:
        file.write(tensor_to_string(data, separator=separator))


def file_to_tab(path, splitter=None):
    """convert file to matrix"""
    return apply_to_tensor([i.split(splitter) for i in file_to_list(path)], soft_to_float)


def file_split(path):
    """takes dec file and splits it in dec list of lists keeping strings together (removes blank lines)"""
    return [x.split() for x in read_file(path).split("\n") if x != '']


def save_obj(obj, path):
    """save obj as pickle file"""
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load_obj(path):
    """load obj from pickle file"""
    with open(path, "rb") as f:
        return pickle.load(f)
