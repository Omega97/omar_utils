from omar_utils.file_basics import write_file, file_to_tab


def data_gen(path, f, inputs):
    """ :return list of input-output lists, output is calculated using f"""
    write_file(path, [[i, f(i)] for i in inputs])


if __name__ == "__main__":

    def f(v):
        return sum([i**2 for i in v])

    V = [i for i in range(3)]
    Name = 'data.txt'

    data_gen(Name, f, V)

    print(file_to_tab(Name))
