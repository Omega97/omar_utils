"""
In this simple example the computation
consists of increasing self.n by +1


"""
from data.computation import *
from os import remove


class New(Computation):

    def __init__(self, path: str):
        self.n = 0
        super().__init__(path)

    def execute(self, n):
        """the operations"""
        for _ in range(n):
            self.n += 1
            print(self.n)


data_path = 'data.pkl'

# start computation
comp = New(data_path)
print('start')
comp.execute(4)
comp.save()
del comp    # just to make sure it's really gone, unnecessary

print('pause')

# resume computation later
comp = New(data_path)
comp = comp.load()
comp.execute(4)
comp.save()

print('end')
remove(data_path)   # just because I don't want to leave random files out there
