""" URL_utils

File uses a url and a path
When initialized, tries to load the file
If unsuccessful, tries to download data from the web

"""
from urllib import request
from omar_utils.basic.tensors import *
from omar_utils.basic.file_basics import write_file, read_file
import os


class File:
    def __init__(self, url=None, path=None, separator=''):
        self.path = path
        self.url = url
        self.data = None
        self.separator = separator
        self.index_ = 0
        self.load()

    def save(self, path=None, separator='\t'):
        """save data in a file"""
        if path:
            self.path = path
        if self.path:
            print('>>>  Saving data in file "%s"\n' % self.path)
            # create dirs
            dirs = self.path.split('/')[:-1]
            for i in range(len(dirs)):
                p = '/'.join(dirs[:(i+1)])
                if not os.path.isdir(p):
                    os.mkdir(p)
            # create file
            s = '\n'.join([separator.join([j for j in i]) for i in self.data])
            write_file(self.path, s)
        else:
            raise TypeError('Please specify the path!')

    def load_from_file(self, path=None, separator=''):
        """load data form file using the path, self.data -> matrix"""
        if path:
            self.path = path
        if separator != '':
            self.separator = separator
        if self.data is None and self.path is not None:
            self.data = read_file(self.path)
            if self.separator != '':
                self.data = [i.split(self.separator) for i in self().split('\n')]
            else:
                self.data = [[i] for i in self().split('\n')]

    def download_data(self, url=None, encoding="UTF-8", separator=''):
        """download data form the web using the URL, self.data -> matrix"""
        if url:
            self.url = url
        self.data = request.urlopen(self.url).read().decode(encoding)
        self.to_tab(separator)

    def load(self, separator=''):
        print('\n>>>  Loading file...')
        try:
            if self.path is not None:
                print('>>>  Trying to load data from "%s"' % self.path)
                self.load_from_file(separator=separator)
            if self():
                if self.url:
                    print('>>>  An URL has been provided, but data has been loaded from "%s" anyway' % self.path)
                print('>>>  Loaded data from file "%s"\n' % self.path)
        except FileNotFoundError:
            pass

        if self() is None:
            if self.url:
                print('>>>  Trying download...')
                self.download_data()
            if self():
                print('>>>  Downloaded data from "%s"\n' % self.url)
                if separator != '':
                    self.split(separator)

        if self() is None:
            raise FileNotFoundError

    def to_tab(self, separator=''):
        if type(self()) == str:
            if separator != '':
                self.data = string_to_matrix(self.data, separator=separator)
            else:
                self.data = [[i] for i in self().split('\n')]
        return self

    def split(self, separator=None):  # make sure mat
        if type(self()) == list:
            self.data = [i[0].split(separator) for i in self.data]
        return self

    def to_float(self):
        if type(self()) == list:
            self.data = tensor_soft_to_float(self())
        return self

    def __call__(self, *args, **kwargs):
        return self.data

    def __len__(self):
        if self() is None:
            return 0
        return len(self())

    def __getitem__(self, item):
        return self()[item]

    def __iter__(self):
        self.index_ = 0
        return self

    def __next__(self):
        out = self[self.index_]
        self.index_ += 1
        if self.index_ >= len(self):
            raise StopIteration
        return out


if __name__ == '__main__':

    URL = 'https://raw.githubusercontent.com/Omega97/google_hash/master/example/problems/a_example.txt'
    PATH = 'data/data1.txt'

    file_ = File(url=URL, path=PATH)
    file_.split()
    # file_.save(separator=' ')

    if file_:
        for I in file_:
            print('\t'.join(I))
