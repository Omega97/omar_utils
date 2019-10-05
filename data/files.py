"""         URL_utils

File(url, path)
.data: str
.tab: pd.DataFrame
When initialized, tries to load the file as string to .data
If unsuccessful, tries to download data from the web (as string to .data)
"""
from urllib import request, error
from omar_utils.basic.file_basics import write_file, read_file
import os
import pandas as pd
from omar_utils.basic.tensors import soft_to_float


class File:
    def __init__(self, url=None, path=None, separator=None, do_report=False, encoding="UTF-8"):
        self.path = path
        self.url = url
        self.data = None
        self.tab = None
        self.separator = separator
        self.do_report = do_report
        self.encoding = encoding
        self.loading_sequence()

    def report(self, message, s='>>>  ', pre_new_line=0):
        """fancy print, but only if self.do_report"""
        if self.do_report:
            print('\n' * pre_new_line + s + message)

    def is_loaded(self):
        """:return True if data has been loaded"""
        return self.data is not None

    def save(self, path=None):
        """save data in a file as string"""

        # preparation
        if path:
            self.path = path
        if not self.path:
            raise TypeError('Please specify the path before saving!')
        if not self.data:
            raise TypeError('Please load some data before saving!')

        # create dirs
        self.report('Saving data in file "%s"\n' % self.path)
        dirs = self.path.split('/')[:-1]
        for i in range(len(dirs)):
            p = '/'.join(dirs[:(i+1)])
            if not os.path.isdir(p):
                os.mkdir(p)

        # create file
        write_file(self.path, self.data)

        return self

    def gen_tab(self):
        """use .data to generate .tab DataFrame"""
        if self.separator != '':
            v = [i.split(self.separator) for i in self.data.split('\n')]
            v = [i for i in v if len(i)]
            self.tab = pd.DataFrame(v)
        else:
            self.tab = pd.DataFrame([[i] for i in self.data.split('\n')])

    def load_from_file(self, path=None):
        """load data form file using the path, self.data -> matrix"""
        if path:
            self.path = path

        # load .data and .tab
        if self.path is not None:   # if a path has been specified
            self.data = read_file(self.path)
            self.gen_tab()

    def download_data(self, url=None):
        """download data form the web using the URL, self.data -> matrix"""
        if url:
            self.url = url
        self.data = request.urlopen(self.url).read().decode(self.encoding)
        if self.is_loaded():
            self.gen_tab()

    def loading_sequence(self):
        """
        1)
        if path has been provided:
            try to load data from .path
        2)
        if no data has been loaded:
            if url has been provided:
                download data from web
        3)
        if still no data has been loaded:
           raise error
        """
        self.report('Loading file...', pre_new_line=1)

        # 1) try to load data from .path
        if self.path is not None:
            self.report('Trying to load data from "%s"' % self.path)
            try:
                self.load_from_file()   # loading...
                self.report('Loaded data from file "%s"' % self.path)
                if self.is_loaded() and self.url:
                    self.report('An URL has been provided, but data has been loaded from locally anyway')
            except FileNotFoundError:
                self.report('Cannot load data from "%s"' % self.path)

        # 2) try to download data from .url
        if not self.is_loaded():
            if self.url:
                self.report('Trying to download data from "%s"' % self.url)
                try:
                    self.download_data()    # downloading...
                    self.report('Downloaded data from "%s"' % self.url)
                except error.URLError:
                    self.report('Cannot download data from "%s"' % self.url)

        # 3) still no data has been loaded
        if not self.is_loaded() and (self.path or self.url):
            message = '\n- Cannot load data from "%s"' % self.path
            message += '\n- Cannot download data from "%s"' % self.url
            message += '\n\n Please check:'
            message += '\n- file path'
            message += '\n- URL'
            message += '\n- internet connection'
            raise FileNotFoundError(message)
        else:
            if self.is_loaded():
                if len(self) < 10**3:
                    message = '%d B' % len(self)
                else:
                    message = '%f kB' % round(len(self)/1000, 3)
                self.report('Data has been successfully loaded (' + message + ')\n')
            else:
                self.report('Warning: This file is empty, use .load_from_file or .download_data to load data')

    def __call__(self) -> pd.DataFrame:
        return self.tab

    def __len__(self):
        if self.is_loaded():
            return len(self.data)
        else:
            return 0

    def __getitem__(self, item):
        return self()[item]

    def __iter__(self):
        return iter(self())

    def __next__(self):
        return next(self())

    def __repr__(self):
        return str(self())

    def apply(self, func):
        """apply func on .tab"""
        for i in self.tab:
            for j in range(len(self.tab[i])):
                self.tab[i][j] = func(self.tab[i][j])

    def to_float(self):
        # self.apply(soft_to_float)
        self.apply(soft_to_float)


if __name__ == '__main__':

    from omar_utils.basic.file_basics import del_file

    URL = 'https://raw.githubusercontent.com/Omega97/google_hash/master/example/problems/a_example.txt'
    PATH = 'data1.txt'

    del_file(PATH)

    f = File(url=URL, path=PATH, do_report=True)
    f.to_float()
    print(f)
    f.save()

    f = File(path=PATH, do_report=True)
    print(f)

    f = File(url=None, path=None, do_report=True)
    print(f)
