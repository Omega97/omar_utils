""" Basic operations with files"""
from os import makedirs, listdir, remove
from basic.tensors import tensor_to_string, apply_to_tensor, soft_to_float
import shutil


def write_file(path, text):
    """ rewrite file"""
    with open(path, 'w') as file:
        file.write(text)
        file.close()


def append_file(path, text, new_line='\n'):
    """append text to file"""
    with open(path, 'a') as file:
        file.write(new_line + text)
        file.close()


def make_dir(path):
    """create directory"""
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


def del_file(path):
    """ delete file """
    path = add_file_extension(path)
    remove(path)


def list_files_in_dir(path):
    """ :returns list of files in path, None if path not found (./ indicates the dir of the file) """
    try:
        return listdir(path)
    except FileNotFoundError:
        return


def file_to_list(path):
    """takes dec file and splits it in dec list of lists dividing strings (removes blank lines)"""
    v = [x for x in read_file(path).split('\n') if x != '']
    return apply_to_tensor(v, soft_to_float)


def list_to_file(path, v):
    """"""
    write_file(path, '\n'.join(apply_to_tensor(v, str)))


def tab_to_file(path, data, tab='\t'):
    """" save tensor in file """
    path = add_file_extension(path)
    file = open(path, 'w')
    file.write(tensor_to_string(data, tab=tab))
    file.close()


def file_to_tab(path, splitter=None):
    """convert file to matrix"""
    return apply_to_tensor([i.split(splitter) for i in file_to_list(path)], soft_to_float)


def file_split(path):
    """takes dec file and splits it in dec list of lists keeping strings together (removes blank lines)"""
    return [x.split() for x in read_file(path).split("\n") if x != '']


def add_file_extension(path):
    """ 'path' -> 'path.txt' """
    if len(path.split('.')) == 1:
        return path + '.txt'
    else:
        return path


def read_file(path):
    """output file content as list"""
    path = add_file_extension(path)
    try:
        file = open(path)
    except FileNotFoundError:
        print('File', path, 'not found')
        return
    return ''.join([i for i in file])


if __name__ == "__main__":

    Name = 'data.txt'
    write_file(Name, 'a b c\n1 2 3')
    append_file(Name, 'new')
    Data = file_to_list(Name)
    print(Data, '\n')
    Data = file_to_tab(Name)
    print(Data, '\n')
    del_file(Name)

    Name = 'data.txt'
    tab_ = [[1, '2'], ['c', 'D']]
    tab_to_file(Name, tab_)
    print(file_to_tab(Name))
    del_file(Name)
