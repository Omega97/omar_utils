"""
useful tensor methods
26/2/2019
"""
from math import log2
from random import random


def tensor_depth(v):
    """ :returns max depth of a tensor (1 -> 0 ; [1] -> 1 ; [[1], 2] -> 2)"""
    return 0 if type(v) != list else max([tensor_depth(i) for i in v]) + 1


def void_tensor(v, fill=0.):
    """ replace all non-list components of a tensor with "fill" """
    return fill if type(v) != list else [void_tensor(i) for i in v]


def is_vector(m):
    """ test if m is a vector """
    if type(m) != list:
        return False
    else:
        if len(m) < 1:
            return False
    if sum([(type(i) == list) for i in m]) > 0:
        return False
    return True


def is_matrix(m):
    """ test if m is a matrix """
    if type(m) != list:
        return False
    else:
        if len(m) < 1:
            return False
        if sum([1-is_vector(i) for i in m]) > 0:
            return False
        v = [len(i) for i in m]
        return True if len(m) == min(v) == max(v) else False


def display_tensor(m, depth=0):
    """ useful to print a tensor """
    if type(m) == list:
        if len(m) > 0:
            for i in m:
                display_tensor(i, depth=depth + 1)
        else:
            print(' .  ' * (depth+1))
    else:
        print(' .  ' * depth, m)


def tensor_sum(v):
    """ sum all elements in v """
    sum_ = 0

    if type(v) == float or type(v) == int:
        sum_ += v

    else:
        if type(v) == list:
            for i in v:
                sum_ += tensor_sum(i)

    return sum_


def tensor_scalar_add(v, x):
    """ add x to all elements in v """
    if type(v) == float or type(v) == int:
        v += x
    else:
        if type(v) == list:
            for i in range(len(v)):
                v[i] = tensor_scalar_add(v[i], x)

    return v


def tensor_scalar_prod(v, x):
    """ multiply all elements in v by x """
    if type(v) == float or type(v) == int:
        v *= x
    else:

        if type(v) == list:
            for i in range(len(v)):
                v[i] = tensor_scalar_prod(v[i], x)

    return v


def tensor_add(v, w):
    """ element-wise sum of tensors """
    if (type(v) == float or type(v) == int) or (type(w) == float or type(w) == int):
        return v + w
    if type(v) == type(w) == list:
        return [tensor_add(v[i], w[i]) for i in range(len(v))]


def tensor_sub(v, w):
    """ element-wise subtraction of tensors """
    return tensor_add(v, tensor_scalar_prod(w, -1))


def tensor_prod(v, w):
    """ element-wise product of tensors """
    if (type(v) == float or type(v) == int) or (type(w) == float or type(w) == int):
        return v * w
    if type(v) == type(w) == list:
        return [tensor_prod(v[i], w[i]) for i in range(len(v))]


def tensor_count(v, x=None):
    """ count the number of elements in v """
    sum_ = 0

    for i in v:
        if type(i) == list:
            sum_ += tensor_count(i, x=x)
        else:
            if x is None:
                sum_ += 1
            else:
                if i == x:
                    sum_ += 1

    return sum_


def tensor_max(v):
    """ max element in tensor """
    max_ = ''

    if type(v) == float or type(v) == int:
        if max_ is '':
            max_ = v
        else:
            max_ = max(max_, v)
    else:
        if type(v) == list:
            if max_ is '':
                w = []
                for i in v:
                    x = tensor_max(i)
                    if x is not '':
                        w += [x]
                max_ = max(w) if len(w) > 0 else ''
            else:
                max_ = max([max_] + [tensor_max(i) for i in v])   # todo not float nor int >> is list >> max_ is not ''

    return max_


def tensor_min(v):
    """ min element in tensor """
    min_ = ''

    if type(v) == float or type(v) == int:
        if min_ is '':
            min_ = v
        else:
            min_ = min(min_, v)
    else:
        if type(v) == list:
            if min_ is '':
                w = []
                for i in v:
                    x = tensor_max(i)
                    if x is not '':
                        w += [x]
                min_ = min(w) if len(w) > 0 else ''
            else:
                min_ = min([min_] + [tensor_max(i) for i in v])

                # todo  not float nor int >> is list >> max_ is not ''

    return min_


def tensor_positive(v):
    """ all negative elements become 0. """
    if type(v) == float or type(v) == int:
        return max(0., v)
    else:
        if type(v) == list:
            return [tensor_positive(i) for i in v]
    return v


def normalize_tensor(v):
    """ sum of all values is 1 """
    v = tensor_positive(v)
    s = tensor_sum(v)
    if s != 0:
        return tensor_scalar_prod(v, 1/s)
    else:
        a = tensor_min(v)
        if a == 0:
            a = 1
        return normalize_tensor(tensor_scalar_add(v, a))


def redistribute_tensor(v, k):
    """ k -> +1 distribution tents to collapse; k -> 0 noting happens; k -> -1 uniform distribution """
    max_ = tensor_max(v)
    tensor_scalar_add(v, -max_ * log2(1 + k))
    return normalize_tensor(v)


def collapse_tensor(v, **kwargs):
    """ collapse distribution tensor v to one-hot tensor """
    first_call = False if 'first_call' in kwargs else True
    count = kwargs['count'] if 'count' in kwargs else random()
    collapsed = kwargs['collapsed'] if 'collapsed' in kwargs else False
    w = []

    if first_call:
        v = normalize_tensor(v)

    for i in v:
        # if a number
        if type(i) == float or type(i) == int:
            if collapsed:
                w.append(0)
            else:
                count -= i
                if count <= 0.:
                    w.append(1)
                    collapsed = True
                else:
                    w.append(0)
        # if a list
        elif type(v) == list:
            new_w, new_args = collapse_tensor(i, count=count, first_call=False, collapsed=collapsed)
            w.append(new_w)
            count = new_args['count']
            collapsed = new_args['collapsed']
        # otherwise
        else:
            w.append(i)

    if first_call:
        return w
    else:
        return w, {'first_call': False, 'count': count, 'collapsed': collapsed}


def pick_element_n(v, n, aux=0):
    """
    convert tensor of binary values into 1-hot tensor (n-th element is a 1, those that are 0 are not counted)
    :param v: tensor of binary values
    :param n: index of element to pick
    :param aux: current count of elements
    :return: 1-hot tensor (the n-th element is a 1)
    """
    w = []

    for i in v:
        if type(i) == int or type(i) == float:
            if i == 1:
                if aux == n:
                    w.append(1)
                else:
                    w.append(0)
                aux += 1
            else:
                w.append(0)
        elif type(i) == list:
            new = pick_element_n(i, n, aux=aux)
            aux += tensor_count(i, x=1)
            w.append(new)
    return w


def apply_to_tensor(v, fun):
    """ applies fun to each element in v """
    if type(v) == list:
        return [apply_to_tensor(i, fun) for i in v]
    else:
        try:
            return fun(v)
        except ValueError:
            return v


def to_float(v):
    """ change type of each element in v to float """
    return apply_to_tensor(v, float)


def to_int(v):
    """ change type of each element in v to int """
    return apply_to_tensor(v, int)


def to_str(v):
    """ change type of each element in v to str """
    return apply_to_tensor(v, str)


def tensor_to_string(v, depth=0):
    """ convert a tensor into a neat string """
    s = ''
    if type(v) == list:
        for i in v:
            s += tensor_to_string(i, depth=depth+1)
        s += '\n'
    else:
        s += str(v) + '\t'

    if depth == 0:
        while s[-1] == '\n':
            s = s[:-1]
        s += '\n'

    return s


def zeros(v, initial_val=0.):
    """ :return a matrix of dimension v[1] x v[2] x v[3] ... x v[n] with values set to initial_val """
    if type(v) == int:
        return zeros([v])
    a = initial_val
    if type(v) == list:
        for i in v:
            a = [a for _ in range(i)]
    return a


def replace_char(st, chars, swap=False):    # todo generalize to "replace"
    """
    replace chars in st
    chars = ['a', 'b'] would replace 'a' with 'b'
    chars = [['a', 'b'], ['c', 'd']] would replace 'a' with 'b' and 'c' with 'd'

    :param st: can be string or list
    :param chars: ['a', 'b'] or [['a', 'b'], ['c', 'd']]
    :param swap: swap chars instead of replacing
    :return:
    """

    if type(st) == str:
        if is_vector(chars):
            if swap:
                return replace_char(st, [[chars[0], '§'], [chars[1], chars[0]], ['§', chars[1]]])
            else:
                return ''.join([i if i != chars[0] else chars[1] for i in st])
        else:
            if type(chars) == list:
                for i in chars:
                    st = replace_char(st, i, swap=swap)
                return st
    elif type(st) == list:
        return [replace_char(i, chars, swap=swap) for i in st]


def cut_matrix(v, xy_from, xy_to):  # todo rows columns?
    """ :return a rectangular matrix with same elements of v, but smaller """
    if xy_to[0] < 0:
        xy_to[0] += len(v[0])
    if xy_to[1] < 0:
        xy_to[1] += len(v)
    return [[v[j][i] for i in range(xy_from[0], xy_to[0]+1)] for j in range(xy_from[1], xy_to[1]+1)]


if __name__ == "__main__":
    ...
    assert zeros(4) == [0.0, 0.0, 0.0, 0.0]
    assert zeros([4], initial_val=2) == [2, 2, 2, 2]
    assert zeros([2, 2]) == [[0.0, 0.0], [0.0, 0.0]]

    assert replace_char('123', ['2', '0']) == '103'
    assert replace_char('123', [['1', 'a'], ['2', 'b'], ['3', 'c']]) == 'abc'
    assert replace_char('123', ['1', '3'], swap=True) == '321'
    assert replace_char('12--34', [['1', '4'], ['2', '3']], swap=True) == '43--21'  # swap 1 with 4 and 2 with 3

    N = 4
    V = [[J + N * I for J in range(N - 1)] for I in range(N)]
    for _ in V:
        print(_)

    print()
    V = cut_matrix(V, [0, 0], [-1, -2])

    for _ in V:
        print(_)
