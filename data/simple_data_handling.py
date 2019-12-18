"""Simple data handling"""
from omar_utils.basic.files import file_to_tab, tab_to_file


def save_data(path, data):
    """save list on file"""
    tab_to_file(path, data)


def load_data(path, splitter=None):
    """ load data form file as a float matrix """
    return file_to_tab(path, splitter=splitter)


if __name__ == "__main__":
    from basic.tensors import tensor_to_string

    # gen data
    Data = [(i, i ** 2) for i in range(4)]

    # path
    Name = 'data.txt'

    # save data
    save_data(Name, Data)

    # load data
    Data = load_data(Name)
    print(tensor_to_string(Data))
