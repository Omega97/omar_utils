

def apply_to_tuple(t, f):
    """ :return tuple """
    v = ()
    for i in t:
        v += (f(i),)
    return v


if __name__ == "__main__":

    assert apply_to_tuple((1, 2, 3), str) == ('1', '2', '3')
