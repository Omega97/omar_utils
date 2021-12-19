
"""         Data handling
The File class:
1) Tries to load data from self.path (if path provided)
2) Tries to download data from web (if no data loaded but URL provided)
"""
__author__ = "Omar Cusma Fait"
__date__ = (19, 12, 2021)
__version__ = "1.0.0"


import pandas as pd


class Data:
    """"Load data, compute fit"""
    def __init__(self, data=None, path=None, url=None, load_method=pd.read_csv):
        self.data = data
        self.path = path
        self.url = url
        self.load_method = load_method
        self.load_data()

    def __repr__(self):
        if self.data is None:
            return 'Data()'
        else:
            return str(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def set_data(self, data):
        self.data = data

    def get_data(self) -> pd.DataFrame:
        return self.data

    def save(self, path=None, index=False):
        if path is None:
            path = self.path
        self.get_data().to_csv(path, index=index)

    def load_data(self):
        """if self.data is empty then try to load data from file"""
        if self.data is None:
            if self.path is not None:
                # try loading local file
                self.set_data(self.load_method(self.path))
            elif self.url is not None:
                # try loading local file
                self.set_data(self.load_method(self.url))
                self.save()
