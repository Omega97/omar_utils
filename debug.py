"""
                    Debug

Add the @Debug() decorator on top of any method.
This will show you:
- when it is called
- the input args and kwargs
- the output
- when it returned the output
- the nested structure of all calls
"""


def debug_print(s='', indent=0):
    """pretty-print string s"""
    print(Debug.separator * (Debug.count + indent) + ' ' + s)


def pre_print(fun, args, kwargs):
    """print name of the function and arguments"""
    a_ = [str(i) for i in args]
    k_ = [str(i) + "=" + str(kwargs[i]) for i in kwargs]
    s = f'{fun.__name__}(' + f'{", ".join(a_ + k_)}' + ')'
    debug_print()
    debug_print(s)
    Debug.count += 1


def post_print(out):
    """print the output of the function"""
    s = f'{out}'
    Debug.count -= 1
    debug_print(indent=1)
    debug_print(s)


class Debug:

    count = 0
    separator = ' .  '

    def __call__(self, fun):
        def wrap(*args, **kwargs):
            pre_print(fun, args, kwargs)
            out = fun(*args, **kwargs)
            post_print(out)
            return out
        return wrap
