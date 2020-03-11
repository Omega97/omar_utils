"""
Pause and resume computations by storing relevant data in files

A computation transforms old parameters into new ones
computation(old_par): -> new_par

This procedure is repeated "steps" times, then data is displayed and saved
The whole process is repeated "repeat" times

Data is stored in a file of the same name of the method used to compute them.
To avoid collisions, provide a custom name
Computation(name='example', ...)

"""
# todo add time to "execute"
import pickle
from random import random
import os
import inspect


def get_args(f):
    return tuple(inspect.signature(f).parameters)[:f.__code__.co_argcount]


def accepts_kwargs(f):
    for i in str(inspect.signature(f))[1:-1].split(', '):
        if i.startswith('**'):
            return True        
    return False


def check(fun, dct):    
    if type(dct) != dict:
        raise TypeError(f'"{fun.__name__}" must return a dict')

    var_names = get_args(fun)

    # if fun accepts kwargs -> use all dct
    if accepts_kwargs(fun):
        return fun(**dct)
    
    for i in var_names:
        if i not in dct:
            message = '\n'
            message += 'Missing parameter\n'
            message += f'method "{fun.__name__}" requires "{i}"\n'
            message += 'provided:\n'
            message += str(dct) + '\n'
            raise TypeError(message)
    return fun(**{i: dct[i] for i in var_names})


def reset_computation(name):
    """restart computation by deleting related data"""
    try:
        os.remove(name + '.pkl')
    except FileNotFoundError:
        pass


class Computation:

    def __init__(self, computation_method, name=None, initial_par=None, display_data=None, show=True):
        """
        :param name: name associated with the computation, used as name of file where data is stored
        :param computation_method: here is where the computation happens, transforms parameters into new ones
        :param initial_par: initial parameters
        :param display_data: method: parameters -> str; used to display parameters
        """
        self.computation_method = computation_method
        self.name = name if name else computation_method.__name__
        self.init_par = initial_par
        self.display_method = display_data if display_data else lambda **kw: str(kw)
        self.data = None
        self.show = show
        self.display(f'\n\nInitializing "{self.name}"\n')

        # try to resume computation
        self.retrieve_data()

        # else start new computation
        if self.data is None:
            self.data = self.init_par

    def display(self, s):
        if self.show:
            print(s)

    def path(self):
        return f'{self.name}.pkl'

    def retrieve_data(self):
        """try to load data from file"""
        try:
            with open(self.path(), "rb") as f:
                self.data = pickle.load(f)
                self.display('Data loaded successfully!\n')
        except FileNotFoundError:
            pass

    def _save_data(self):
        """ save self.data in file"""
        with open(self.path(), "wb") as f:
            pickle.dump(self.data, f)

    def compute(self):
        """make ONE computation (par -> new par)"""
        # check all parameters in self.data are OK
        self.data = check(self.computation_method, self.data)

    def execute(self, steps, repeat=1):
        """
        execute computation
        :param steps: each block executes the computation "steps" times
        :param repeat: there are "repeat" blocks, data is saved at the end of each one (-1 to repeat indefinitely)
        """
        self.display(f'computing "{self.name}"\n')

        # check that a dict was loaded into self.data
        try:
            assert type(self.data) == dict
        except AssertionError:
            message = 'Data has been imported improperly!\n'
            message += '\nloaded data:\n'
            message += f'{self.data}\n'
            message += '\nexpected: dict\n'
            raise TypeError(message)

        while repeat:
            repeat -= 1
            for _ in range(steps):
                self.compute()
            self._save_data()
            self.display(self)

    def get_result(self):
        return self.data

    def __repr__(self):
        return check(self.display_method, self.data)


def compute_average(fun, steps, repeat=1, initial_value=0., show=True):
    """fun just returns a value, compute the average of those values"""
    name = fun.__name__

    def compute_number(n, x):
        new = fun()
        return {'n': n+1, 'x': x * n/(n+1) + new/(n+1)}

    def display_number(n, x):
        if show:
            return f'avg = {x} \t n = {n}'
        else:
            return f'n = {n}'

    comp = Computation(name=name,
                       computation_method=compute_number,
                       initial_par={'n': 0, 'x': initial_value},
                       display_data=display_number)

    comp.execute(steps=steps, repeat=repeat)

    return comp.data['x']


# ------------ Examples ----------------------------------------------------------------------------------------


def example_0():
    """ Value Error"""
    def compute_number(n, x):
        """transform old parameters into new ones"""
        return {'n': n + 1, 'x': x + random()}

    def display_number(n, x):
        """transform parameters onto readable outputs"""
        return f'ang = {x / n:.6f} \t n = {n}'

    comp = Computation(computation_method=compute_number,
                       initial_par={'x': 0, 'n': 0},
                       display_data=display_number)

    comp.execute(steps=10**4, repeat=3)


def example_1():
    """compute pi"""
    reset_computation('compute_slow_pi')    # restart computation by deleting data

    def compute_slow_pi(n, s):
        return {'n': n + 1, 's': s + (-1) ** n / (2*n+1)}

    def display_slow_pi(n, s):
        return f'\n{"pi":>5} = {s * 4}\n{"n":>5} = {n}'

    comp = Computation(computation_method=compute_slow_pi,
                       initial_par={'n': 0, 's': 0},
                       display_data=display_slow_pi)

    comp.execute(steps=10**4, repeat=3)


def example_2():
    """ Value Error"""
    def compute_number_2(n, x, s):
        x = 1 + random() / x
        return {'x': x, 's': s + x, 'n': n + 1}

    def display_number(n, s):
        return f'{s / n:.7f} \t {n}'

    comp = Computation(name='_example_2',
                       computation_method=compute_number_2,
                       initial_par={'x': 1, 's': 0, 'n': 0},
                       display_data=display_number)

    comp.execute(steps=10**4, repeat=3)


def example_3():
    """ Value Error"""
    def compute_number_3():
        new = random()
        return new

    compute_average(compute_number_3, steps=10**4, repeat=3)


if __name__ == '__main__':

    # Example
    example_0()
    # example_1()
    # example_2()
    # example_3()
