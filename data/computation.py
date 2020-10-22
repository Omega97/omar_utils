"""
                        Computation


Subclass this to allow to save and load object,
so you can pause and later resume computations

save -  save object in a file, useful if you want to resume
        some computation later

load -  load object from a file

"""
import pickle


class Computation:

    def __init__(self, path):
        self.path = path

    def save(self):
        """save object in file"""
        with open(self.path, "wb") as f:
            pickle.dump(self, f)

    def load(self):
        """set all attributes of "self" equal to the attributes of the loaded object
        Note: it does NOT overwrite self
        """
        with open(self.path, "rb") as f:
            return pickle.load(f)

    def execute(self, *args, **kwargs):
        """ Here is where the actual computation happens """
        raise NotImplementedError
