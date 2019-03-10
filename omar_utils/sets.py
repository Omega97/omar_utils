from copy import copy


# todo args? decorators?


def empty_set():
    return set()


def to_set(v):
    return set(v) if type(v) == list else {v}


def join_sets(v):
    aux = empty_set()
    for i in v:
        aux.update(i)
    return aux


def remove_from_set(a, element):
    try:
        out = copy(a)
        out.discard(element)
        return out
    except KeyError:
        pass


def subtract_sets(a, v):
    if type(v) == list:
        return a - join_sets(v)
    else:
        return a - v


def intersect_sets(v):
    aux = v[0]
    for i in v:
        aux = aux.intersection(i)
    return aux


if __name__ == "__main__":

    A = {1, 2, 3}
    B = {2, 3, 4}
    C = {3, 4, 5}

    A0 = copy(A)
    B0 = copy(B)
    C0 = copy(C)

    print(intersect_sets(A, B))

    assert A == A0
    assert B == B0
    assert C == C0
