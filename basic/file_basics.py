""" Basic operations with files"""
from os import makedirs, listdir, remove
from omar_utils.basic.tensors import tensor_to_string, apply_to_tensor, soft_to_float
import shutil


def write_file(path, text, encoding='utf-8'):
    """rewrite file"""
    with open(path, "w", encoding=encoding) as file:
        file.write(text)
        file.close()


def read_file(path, encoding='utf-8') -> str:
    """output file content as list"""
    with open(path, encoding=encoding) as file:
        return file.read()


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
    try:
        remove(path)
    except FileNotFoundError:
        pass


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
    """list -> file"""
    write_file(path, '\n'.join(apply_to_tensor(v, str)))


def tab_to_file(path, data, separator='\t'):
    """" save tensor in file """
    file = open(path, 'w')
    file.write(tensor_to_string(data, separator=separator))
    file.close()


def file_to_tab(path, splitter=None):
    """convert file to matrix"""
    return apply_to_tensor([i.split(splitter) for i in file_to_list(path)], soft_to_float)


def file_split(path):
    """takes dec file and splits it in dec list of lists keeping strings together (removes blank lines)"""
    return [x.split() for x in read_file(path).split("\n") if x != '']


if __name__ == "__main__":

    Name = 'data.txt'

    write_file(Name, 'a b c\n1 2 3')
    append_file(Name, 'new')
    Data = file_to_list(Name)
    assert Data == ['a b c', '1 2 3', 'new']
    assert file_to_tab(Name) == [['a', 'b', 'c'], [1, 2, 3], ['new']]
    del_file(Name)

    Tab = [[1, '2'], ['c', 'D']]
    tab_to_file(Name, Tab)
    assert file_to_tab(Name) == [[1, 2], ['c', 'D']]
    del_file(Name)

    Text = '古'
    write_file(Name, Text)
    assert read_file(Name) == '古'
    assert type(read_file(Name)) == str
    del_file(Name)
