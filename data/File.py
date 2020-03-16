"""         Data handling
The File class:
1) Tries to load data from self.path (if path provided)
2) Tries to download data from web (if no data loaded but URL provided)
"""
__author__ = "Omar Cusma Fait"
__date__ = (16, 3, 2020)
__version__ = "2.0.0"
import pandas as pd


class File:
    def __init__(self, path, url, load_method=pd.read_csv, do_report=True):
        self.path = path
        self.url = url
        self.load_method = load_method
        self.do_report = do_report
        self.data = None
        self._load_data()

    def _report(self, s):
        if self.do_report:
            print('>>', s)

    def _load_data(self):
        """
        1) try to load form path
        2) if data not loaded then try to download from url
        :return:
        """
        try:
            self._report('Loading file...')
            self.data = self.load_method(self.path)
            self._report('File successfully loaded!')
        except FileNotFoundError:
            self._report(f'File not found!\n{self.path}')

        if self.data is None:
            try:
                self._report('Downloading file...')
                self.data = self.load_method(self.url)
                self._report('File successfully downloaded!')
                self.save()
                self._report('Data saved!')
            except FileNotFoundError:
                self._report(f'File not found!\n{self.path}')

    def get_data(self) -> pd.DataFrame:
        return self.data

    def save(self):
        self.get_data().to_csv(self.path, index=False)

    def __call__(self, *args, **kwargs):
        return self.data


if __name__ == '__main__':

    def _test_1():
        """download & save & load_file"""
        print('\n\n\t TEST 1 \n')
        url = 'https://raw.githubusercontent.com/Omega97/google_hash/master/example/problems/a_example.txt'
        path = 'data.pkl'
        f = File(url=url, path=path)
        print(f().head())

    _test_1()
