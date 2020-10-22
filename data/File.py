"""         Data handling
The File class:
1) Tries to load data from self.path (if path provided)
2) Tries to download data from web (if no data loaded but URL provided)
"""
__author__ = "Omar Cusma Fait"
__date__ = (22, 10, 2020)
__version__ = "2.1.0"

import pandas as pd


class File:
    def __init__(self, path, url, load_method=pd.read_csv, do_report=True):
        self.path = path
        self.url = url
        self.load_method = load_method
        self.do_report = do_report
        self.data = None
        self.try_load_form_path()
        self.try_to_download_from_url()

    def report(self, s):
        if self.do_report:
            print('>>', s)

    def try_load_form_path(self):
        try:
            self.report('Loading file...')
            self.data = self.load_method(self.path)
            self.report('File successfully loaded!')
        except FileNotFoundError:
            self.report(f'File not found!\n{self.path}')

    def try_to_download_from_url(self):
        try:
            self.report('Downloading file...')
            self.data = self.load_method(self.url)
            self.report('File successfully downloaded!')
            self.save()
            self.report('Data saved!')
        except FileNotFoundError:
            self.report(f'File not found!\n{self.path}')

    def load_data(self):
        self.try_load_form_path()
        if self.data is None:
            self.try_to_download_from_url()

    def get_data(self) -> pd.DataFrame:
        return self.data

    def save(self):
        self.get_data().to_csv(self.path, index=False)

    def __call__(self, *args, **kwargs):
        return self.data
