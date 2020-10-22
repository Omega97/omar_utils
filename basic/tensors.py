"""         Tensors

A lot of useful tensor-related methods

tensor = essentially a list of lists
This library is also an exercise of "list comprehensions"
"""
__author__ = "Omar Cusma Fait"
__version__ = '1.0.2'


def apply_to_tensor(v, fun):
    """ applies fun to each element in v """

    def try_fun(x):
        """try to apply"""
        try:
            return fun(x)
        except ValueError:
            return x

    return [fun(i) if type(i) != list else apply_to_tensor(i, try_fun) for i in v]


def tensor_to_float(v):
    """ change type of each element in v to float """
    return apply_to_tensor(v, float)


def tensor_to_int(v):
    """ change type of each element in v to int """
    return apply_to_tensor(v, int)


def tensor_soft_to_float(v):
    """ change type of each element in v to float """
    return apply_to_tensor(v, soft_to_float)


def to_str(v):
    """ change type of each element in v to str """
    return apply_to_tensor(v, str)


def zeros(v, v0=0):
    """ return tensor of given shape, filled with v0 """
    return [zeros(v[1:], v0=v0) for _ in range(v[0])] if len(v) > 1 else [v0 for _ in range(v[0])]


def tensor_depth(v):
    """ max depth of a tensor   1 -> 0  [1] -> 1    [[1], 2] -> 2 """
    return 0 if type(v) != list else max([tensor_depth(i) for i in v]) + 1


def reset_tensor(v, fill_with=0):
    """ replace all non-list elements of tensor with fill_with """
    return fill_with if type(v) != list else [reset_tensor(i) for i in v]


def is_vector(v):
    """ test if m is vector (list of non list elements) """
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


def tensor_to_string(v, separator='\t', inline='\n'):
    """ convert a tensor into a neat string """
    if type(v) == list:
        if is_vector(v):
            s = separator
        else:
            s = inline * (tensor_depth(v)-1)
        return s.join([tensor_to_string(i, separator, inline) for i in v])
    else:
        return str(v)


def display_tensor(v, separator='\t'):
    """ useful to print a tensor """
    print(tensor_to_string(v, separator=separator))


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
    """ element-wise product_function of tensors """
    if (type(v) == float or type(v) == int) or (type(w) == float or type(w) == int):
        return v * w
    if type(v) == type(w) == list:
        return [tensor_prod(v[i], w[i]) for i in range(len(v))]


def normalize_tensor(v):
    """ sum of all values becomes 1 """
    return tensor_scalar_prod(v, 1/tensor_sum(v))


def almost_equal(v, w, tolerance=10**(-8)):
    """ return True if the difference between 2 tensors is small """
    return tensor_max(apply_to_tensor(tensor_sub(v, w), abs)) <= tolerance


def remove_from_tensor(v, this):
    """ remove "this" from tensor v """
    return [remove_from_tensor(i, this) if type(i) == list else i for i in v if i != this]


def conditioned_remove(v, cond):
    """ remove elements from tensor v that satisfy condition"""
    def f(x):
        return False if type(x) == list else cond(x)
    return [conditioned_remove(i, cond) if type(i) == list else i for i in v if not f(i)]


def round_tensor(v, digits=0):
    """ round the elements in a tensor """
    return [round_tensor(i, digits) if type(i) == list else round(i, digits) for i in v]


def split_tensor(v, separator=None):
    """split elements in v"""
    return [i.split(separator) if type(i) is not list else split_tensor(i, separator) for i in v]


def soft_to_float(x):
    """convert to float if possible, convert to int if x is integer"""
    try:
        return int(x) if int(x) == float(x) else float(x)
    except ValueError:
        return x
    except TypeError:
        return x


def string_to_matrix(s, separator=None):
    """str -> matrix"""
    v = [[j for j in i.split(separator)] for i in s.split('\n')]
    return [i for i in v if i != [''] and i != []]
