""" computation


save - save object in a file, useful if you want to resume some computation later

load - load object from a file

Computation - subclass this to allow to save and load object,
            so you can pause and later resume computations
"""
import pickle
from os import remove


def save(obj, path):
    """save object in a file"""
    with open(path, "wb") as f:
        pickle.dump(obj, f)


def load(path):
    """load object from a file"""
    with open(path, "rb") as f:
        obj = pickle.load(f)
    return obj


def delete(path):
    """delete file"""
    try:
        remove(path)
    except FileNotFoundError:
        pass


class Computation:

    def __init__(self, name, auto_load=True):
        self._name_ = name
        if auto_load:
            self.load()

    def save(self):
        """save object in file"""
        with open(self._name_, "wb") as f:
            try:
                pickle.dump(self, f)
            except AttributeError:
                message = '\n'
                message += f"Can't pickle local object {type(self)}\n"
                message += "Only global objects can be pickled\n"
                raise AttributeError(message)

    def load(self):
        """set all attributes of "self" equal to the attributes of the loaded object"""
        try:
            with open(self._name_, "rb") as f:
                obj = pickle.load(f)
                attr = [i for i in dir(obj) if not (i.startswith('__') and i.endswith('__'))]
                for i in attr:
                    setattr(self, i, getattr(obj, i))
        except FileNotFoundError:
            pass


# ----------------------------------------------------------------------------------------------------


def __test_1():
    # start computation
    a = 0
    a += 1  # computation
    print(a)
    save(a, 'data.pkl')     # <<< save
    del a

    # resume computation
    a = load('data.pkl')    # <<< load
    a += 1  # computation
    print(a)


if __name__ == '__main__':
    # __test_1()

    class New(Computation):
        def __init__(self, name: str, n0=0):
            self.n = n0
            super().__init__(name)

        def execute(self, n):
            for _ in range(n):
                self.n += 1
                print(self.n)

    name_ = 'data.pkl'
    delete(name_)

    # start computation
    comp = New(name_)
    comp.execute(5)     # computation
    comp.save()
    del comp

    # resume computation
    comp = New(name_)
    comp.load()
    comp.execute(5)     # computation
    comp.save()
