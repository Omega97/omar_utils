"""         URL_utils

File(url, path)
.data: str
.tab: pd.DataFrame
When initialized, tries to load the file as string to .data
If unsuccessful, tries to download data from the web (as string to .data)
"""
from urllib import request, error
import os
import pandas as pd
from omar_utils.basic.tensors import soft_to_float, string_to_matrix
from sys import getsizeof


class File:
    def __init__(self, path=None, url=None, separator=None, encoding="UTF-8", do_report=False):
        """
        A File is used to load and store data as pd.DataFrames / .pkl files
        - download data from web as string (data is stored in .data as pd.DataFrame)
        - save data locally in a .pkl file
        - load data from .pkl file to .data as pd.DataFrame

        :param path: used both to load and save .pkl file
        :param url: url
        :param separator: used when downloading from web to split file into columns
        :param encoding: encoding
        :param do_report: do fancy console report
        """
        self.path = None
        self.url = url
        self.data = None
        self.separator = separator
        self.encoding = encoding
        self.do_report = do_report
        self.set_path(path)
        self.loading_sequence()

    def set_path(self, path):
        """make path a .pkl"""
        if path is not None:
            v = path.split('.')
            if len(v) > 1:
                v = v[:-1]
            self.path = '.'.join(v) + '.pkl'

    def report(self, message, s='>>>  ', pre_new_line=0):
        """fancy print, but only if self.do_report"""
        if self.do_report:
            print('\n' * pre_new_line + s + message)

    def report_size(self):
        size = getsizeof(self())
        if size < 1000:
            message = '%d B' % size
        else:
            message = '%.3f kB' % (size / 10 ** 3)
        self.report('Data size = ' + message + '\n')

    def is_loaded(self):
        """:return True if data has been loaded"""
        return self() is not None

    def have_path(self):
        return self.path is not None

    def have_url(self):
        return self.url is not None

    def save(self, path=None):
        """save data in a file as string"""

        # preparation
        self.set_path(path)
        if not self.path:
            raise TypeError('Please specify the path before saving!')
        if not self.is_loaded():
            raise TypeError('Please load some data before saving!')

        # create dirs
        self.report('Saving data in file "%s"' % self.path, pre_new_line=1)
        dirs = self.path.split('/')[:-1]
        for i in range(len(dirs)):
            p = '/'.join(dirs[:(i+1)])
            if not os.path.isdir(p):
                os.mkdir(p)

        # create file
        self().to_pickle(self.path)
        self.report_size()

        return self

    def load_file(self, path=None):
        """load data form file using the path, self.data -> DataFrame"""
        self.set_path(path)
        self.report('Trying to load data from "%s"' % self.path)
        self.data = None
        try:
            # try loading file
            self.data = pd.read_pickle(self.path)
        except AttributeError:
            self.report('File not found!')
        except Exception as e:
            self.report('[' + str(e) + '] error when loading "%s"' % self.path)
        else:
            # file loaded
            self.report('Loaded data from file "%s"' % self.path)
            self.report_size()
            if self.have_url():
                self.report('An URL has been provided, but data has been loaded from locally anyway')

    def download_data(self, url=None):
        """download data form the web using the URL, self.data -> matrix"""
        if url:
            self.url = url
        self.report('Trying to download data from "%s"' % self.url)
        try:
            # try downloading file
            data = request.urlopen(self.url).read().decode(self.encoding)
        except error.URLError:
            self.report('Cannot download data from "%s"' % self.url)
        else:
            # file downloaded
            self.load_var(data)
            self.report_size()

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

        # 1) LOAD data from .path
        if self.have_path():
            self.load_file()    # loading...

        # 2) DOWNLOAD data from .url
        if not self.is_loaded():
            if self.have_url():
                self.download_data()    # downloading...

        # 3) finally...
        if self.is_loaded():
            # loading report
            self.report('Data has been successfully loaded\n')
        else:
            # not loaded...
            if self.have_path() or self.have_url():
                # ...but path/url provided
                message = '\n- Cannot load data from "%s"' % self.path
                message += '\n- Cannot download data from "%s"' % self.url
                message += '\n\n Please check:' + '\n- file path' + '\n- URL' + '\n- internet connection'
                raise FileNotFoundError(message)
            else:
                # ...and path/url not provided
                self.report('Warning: This file is empty, use .load_from_file or .download_data to load data')

    def load_var(self, data):
        """load data from variable, .data must be str"""
        if type(data) == pd.DataFrame:  # DataFrame
            self.data = data
        elif type(data) == list:    # matrix
            self.data = pd.DataFrame(data)
            self.report('Converted list to pd.DataFrame')
        elif type(data) == str:     # string
            try:
                self.data = pd.DataFrame(string_to_matrix(data))
            except Exception as e:
                self.report('[' + str(e) + '] error when converting "%s"' % self.path)
            else:
                self.report('Converted str to pd.DataFrame')
        else:
            self.report('Could not convert data to pd.DataFrame!')

    def __call__(self) -> pd.DataFrame:
        return self.data

    def __len__(self):
        return len(self()) if self.is_loaded() else 0

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
        for i in self():
            for j in range(len(self()[i])):
                self[i][j] = func(self()[i][j])

    def to_float(self):
        self.apply(soft_to_float)

    def del_file(self):
        try:
            os.remove(self.path)
        except FileNotFoundError:
            pass


def test_1():
    """download & save & load_file"""
    print('\n\n\t TEST 1 \n')
    url = 'https://raw.githubusercontent.com/Omega97/google_hash/master/example/problems/a_example.txt'
    path = 'data.pkl'
    os.remove(path)
    f = File(url=url, path=path, do_report=True)
    f.save()
    f.load_file(path)
    print(f)


def test_2():
    """load & save & load_file"""
    print('\n\n\t TEST 2 \n')
    path = 'data.pkl'
    os.remove(path)
    f = File(do_report=True)
    data = pd.DataFrame([[1, 2], [3, 4]], columns=['C1', 'C2'], index=['I1', 'I2'])
    f.load_var(data)
    f.save(path)
    f.load_file(path)
    print(f)


if __name__ == '__main__':
    test_1()
    test_2()
