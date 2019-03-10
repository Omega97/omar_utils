from omar_utils.tuples import apply_to_tuple


def input_is_list(fun):
    """ convert each element of the input into a list """
    def wrapper(*args, **kwargs):
        v = apply_to_tuple(args, lambda x: x if type(x) == list else [x])
        return fun(*v, **kwargs)
    return wrapper



if __name__ == "__main__":


    @input_is_list
    def f(*args, **kwargs):
        print(args)
        print(kwargs)

    print(f(1, 2, [[3]], a=1))
