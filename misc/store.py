
class Store(dict):

    def transform_key(self, key):
        """overwrite to modify the key for __getitem__ and __setitem__"""
        return key

    def compute(self, key):
        """takes the unmodified key as input, returns the value to store in self"""
        raise NotImplementedError

    def __setitem__(self, key, value):
        new_key = self.transform_key(key)
        super().__setitem__(new_key, value)

    def __getitem__(self, key):
        new_key = self.transform_key(key)
        if new_key not in self:
            super().__setitem__(new_key, self.compute(key))
        return super().__getitem__(new_key)
