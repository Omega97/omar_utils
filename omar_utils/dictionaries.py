

def search_key(dic, key):
    # search key in dictionary
    return dic[key] if key in dic else None


def search_keys(dic, keys: list, default=None):
    # search keys in dictionary, replace not found keys with default
    v = [search_key(dic, i) for i in keys]
    if default is None:
        return v
    else:
        return [v[i] if v[i] is not None else default[i] for i in range(len(v))]


def apply_to_dict(dic, fun):
    for i in dic:
        dic.update({i: fun(dic[i])})
    return dic


if __name__ == "__main__":

    D = {'a': 1}

    assert search_key(D, 'a') == 1
    assert search_key(D, 'b') is None
    assert search_keys(D, ['a', 'b'], [0, 0]) == [1, 0]

    D = {'a': 1, 'b': 2}
    assert apply_to_dict(D, lambda x: -x) == {'a': -1, 'b': -2}
