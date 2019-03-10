"""
useful tensor methods
8/3/2019
"""


def tensor_depth(v):
    """ max depth of a tensor   1 -> 0  [1] -> 1    [[1], 2] -> 2 """
    return 0 if type(v) != list else max([tensor_depth(i) for i in v]) + 1


def reset_tensor(v, fill_with=0):
    """ replace all non-list elements of a tensor with fill_with """
    return fill_with if type(v) != list else [reset_tensor(i) for i in v]


def is_vector(v):
    """ test if m is a vector (list of non list elements) """
    if type(v) == list:
        return sum([type(i) == list for i in v]) == 0 and len(v) > 0
    else:
        return False


def is_matrix(m):
    """ test if m is a matrix """
    if type(m) == list:
        return sum([not is_vector(i) for i in m]) == 0 and len(m) > 0
    else:
        return False


def tensor_sum(v):
    """ sum all elements in tensor v """
    return sum([tensor_sum(i) for i in v]) if type(v) == list else v


def add_tensor_float(v, x):
    """ add x to all elements in v """
    return [i + x if type(i) != list else add_tensor_float(i, x) for i in v]


def apply_to_tensor(v, fun):
    """ applies fun to each element in v """
    return [fun(i) if type(i) != list else apply_to_tensor(i, fun) for i in v]


def to_float(v):
    """ change type of each element in v to float """
    return apply_to_tensor(v, float)


def to_int(v):
    """ change type of each element in v to int """
    return apply_to_tensor(v, int)


def to_str(v):
    """ change type of each element in v to str """
    return apply_to_tensor(v, str)


def zeros(v, v0=0):
    """ return tensor of given shape, filled with v0 """
    return [zeros(v[1:], v0=v0) for _ in range(v[0])] if len(v) > 1 else [v0 for _ in range(v[0])]


def replace_in_tensor(v, old, new):
    """ replace all elements equal to old with new"""
    return [replace_in_tensor(i, old, new) if type(i) == list else (new if i == old else i) for i in v]


def clean_tensor(v):
    """ keep only int or floats """
    return [clean_tensor(i) if type(i) == list else i for i in v
            if (type(i) == list or type(i) == int or type(i) == float)]


def join_tensor(v, c=' '):
    """ join all elements of tensor into a string """
    return c.join([join_tensor(i, c=c) if type(i) == list else str(i) for i in v])


def tensor_to_string(v, tab='\t', inline='\n', depth=0):  # todo complete, check
    """ convert a tensor into a neat string """
    s = tab.join([inline + tensor_to_string(i, tab=tab, inline=inline, depth=depth+1) if type(i) == list else str(i)
                  for i in v])
    if not depth:
        while s[0] == inline:
            s = s[1:]
    return s


def display_tensor(v):
    """ useful to print a tensor """
    print(tensor_to_string(v))


def tensor_count(v, equal_to=None):
    """ count the number of elements equal to equal_to  """
    return sum([tensor_count(i, equal_to=equal_to) for i in v]) if type(v) == list else (1 if v == equal_to else 0)


def number_of_elements_in_tensor(v):
    """ count the number of elements in v """
    return sum([number_of_elements_in_tensor(i) for i in v]) if type(v) == list else 1


def conditioned_number_of_elements_in_tensor(v, condition):
    """ count the number of elements in v that satisfy condition """
    return sum([conditioned_number_of_elements_in_tensor(i, condition) for i in v]) if type(v) == list else condition(v)


def negate_tensor(v):
    """ return the tensor with flipped signs """
    if type(v) == list:
        return [negate_tensor(i) for i in v]
    else:
        return -v


def tensor_module(v):
    """ return module of the tensor """
    if type(v) == list:
        return sum([tensor_module(i)**2 for i in v])**.5
    else:
        return abs(v)


def tensor_max(v):
    """ max element in tensor """
    return max([tensor_max(i) for i in v]) if type(v) == list else v


def tensor_min(v):
    """ min element in tensor """
    return min([tensor_min(i) for i in v]) if type(v) == list else v


def tensor_scalar_prod(v, x):
    """ multiply all elements in v by x """
    return [tensor_scalar_prod(i, x) for i in v] if type(v) == list else v * x


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


def normalize_tensor(v):    # todo normalize also the 0 case?
    """ sum of all values becomes 1 """
    return tensor_scalar_prod(v, 1/tensor_sum(v))


def almost_equal(v, w, tolerance=10**(-8)):
    """ return True if the difference between 2 tensors is small """
    return tensor_max(apply_to_tensor(tensor_sub(v, w), abs)) <= tolerance


def remove_from_tensor(v, this):
    """ remove "this" from tensor v """
    return [remove_from_tensor(i, this) if type(i) == list else i for i in v if i != this]


def conditioned_remove(v, cond):    # todo write better?
    """ remove elements from tensor v that satisfy condition"""
    return [conditioned_remove(i, cond) if type(i) == list else i for i in v
            if (not cond(i) if type(i) != list else True)]


# def transpose(m):
#     """ transpose a matrix """
#     size = [max([len(i) for i in m]), len(m)]
#     a = zeros(size)
#     return [[m[i][j] for i in range(len(a[j]))] for j in range(len(a))]


if __name__ == "__main__":

    # TESTS

    # print('-' * 10)
    # print(f([1, 2, 3, 4]))
    # print('-' * 10)
    # print(f([1, 2, [3, 4]]))
    # print('-' * 10)
    # print(f([[1, 2], [3, 4]]))
    # print('-' * 10)
    # print(f([1, [1, [1, [1, [1]]]]]))
    # print('-' * 10)
    # A = 1
    # for I in range(4):
    #     A = [A, A]
    #     print(f(A))
    #     print('-' * 10)

    assert is_vector([1, 2, 3])
    assert not is_vector([1, 2, [1]])
    assert not is_vector(1)
    assert is_matrix([[1, 2], [3, 4]])
    assert not is_matrix(1)
    assert not is_matrix([])
    assert not is_matrix([1, 1])
    assert not is_matrix([1, [1, 1]])
    assert not is_matrix([[1, [1, 1]], [1, 1]])
    assert tensor_sum([1, 2, [3, 4]]) == 10
    assert tensor_scalar_prod(1, 2) == 2
    assert tensor_scalar_prod([1, [2, 3]], .5) == [.5, [1., 1.5]]
    assert add_tensor_float([1, 2], .5) == [1.5, 2.5]
    assert tensor_count([1, [1, 1, 2]], equal_to=1) == 3
    assert number_of_elements_in_tensor([1, [1, 2]]) == 3
    assert conditioned_number_of_elements_in_tensor([1, [1, 3, [4]]], condition=lambda x: x >= 3) == 2
    assert zeros([4], v0=2) == [2, 2, 2, 2]
    assert zeros([3, 2], v0=1) == [[1, 1], [1, 1], [1, 1]]
    assert replace_in_tensor([[1, 2, 3], 3], 3, 'doggo') == [[1, 2, 'doggo'], 'doggo']
    assert join_tensor([1, 'a', [2, [3, 'd', 5]]], c=' ') == '1 a 2 3 d 5'
    assert clean_tensor([1, 2, 'ff', [3, 'd']]) == [1, 2, [3]]
    assert tensor_max([1, [2, 0]]) == 2.
    assert tensor_min([1, [2, 0]]) == 0.
    assert negate_tensor([1, [1, -1]]) == [-1, [-1, 1]]
    assert tensor_module([1, [1, 1, 1]]) == 2
    assert normalize_tensor([1, 2, [1, 2, 4]]) == [.1, .2, [.1, .2, .4]]     # warning
    assert almost_equal(normalize_tensor([1, 2, [3, 4]]), [.1, .2, [.3, .4]])
    assert remove_from_tensor([1, 2, [1, 2]], 1) == [2, [2]]
    assert conditioned_remove([1, 2, [1, 2]], lambda x: x < 2) == [2, [2]]
    assert conditioned_remove([1], lambda x: x > 0) == []
    assert apply_to_tensor([1, [2, 3]], lambda x: x*2) == [2, [4, 6]]

    assert tensor_to_string([1, 1]) == '1\t1'
    assert tensor_to_string([[1, 1], [1, 1]]) == '1\t1\t\n1\t1'
    assert tensor_to_string([[[1, 1], [1, 1]], [[1, 1], [1, 1]]]) == '1\t1\t\n1\t1\t\n\n1\t1\t\n1\t1'

    # assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]
