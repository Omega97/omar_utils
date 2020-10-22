"""         omar_utils

Provides common and useful methods of all kinds
Files are not supposed to depend on one another since they may be frequently updated
"""
from basic import iter_utils
from basic.iter_utils import *
from basic import files
from basic.files import load_obj, save_obj
from test_utils.unit_test import Debug


__author__ = "Omar Cusma Fait"
__date__ = (22, 10, 2020)
__version__ = "1.4.0"


if __name__ == '__main__':
    print('iter_utils', iter_utils.__version__)
    print('files', files.__version__)
    print(i_print, load_obj, save_obj, Debug)
