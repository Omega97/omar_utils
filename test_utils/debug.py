"""
                    Debug

Add the @Debug decorator on top of any method.
This will show you:
- where it was called
- it's inputs
- where it returned
- it's output
- the nested structure of all calls
# todo generators
"""


class Debug:

    count = 0

    def __init__(self, fun, separator='|\t'):
        self.fun = fun
        self.out = None
        self.separator = separator

    def _fancy_print(self, s='', indent=0):
        print(self.separator * (Debug.count + indent) + ' ' + s)

    def _pre_print(self, *args, **kwargs):
        s = f'{self.fun.__name__}('
        if len(args):
            s += f'{", ".join([str(i) for i in args])}'
        if len(kwargs):
            s += f', {", ".join([str(i) + "=" + str(kwargs[i]) for i in kwargs])}'
        s += ')'
        self._fancy_print()
        self._fancy_print(s)
        Debug.count += 1

    def _post_print(self):
        s = f'{self.out}'
        Debug.count -= 1
        self._fancy_print(indent=1)
        self._fancy_print(s)

    def __call__(self, *args, **kwargs):
        self._pre_print(*args, **kwargs)
        self.out = self.fun(*args, **kwargs)
        self._post_print()
        return self.out
