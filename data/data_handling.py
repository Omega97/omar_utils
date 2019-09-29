"""Simple data handling"""
from basic.file_basics import file_to_tab, tab_to_file


def save_data(path, data):
    """save list on file"""
    tab_to_file(path, data)


def load_data(path, splitter=None):
    """ load data form file as a float matrix """
    return file_to_tab(path, splitter=splitter)


def data_gen(fun, inputs):
    """  """
    return [[i, fun(i)] for i in inputs]


if __name__ == "__main__":
    from basic.tensors import tensor_to_string

    # gen data
    Data = data_gen(lambda x: x**2, [i for i in range(4)])

    # path
    Name = 'data.txt'

    # save data
    save_data(Name, Data)

    # load data
    Data = load_data(Name)
    print(tensor_to_string(Data))
