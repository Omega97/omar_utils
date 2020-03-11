"""         omar_utils

Provides common and useful methods of all kinds
Files are not supposed to depend on one another since they may be frequently updated
"""
from omar_utils.basic import iter_utils
from omar_utils.basic.iter_utils import *
from omar_utils.basic import files
from omar_utils.basic.files import load_obj, save_obj
from omar_utils.basic.decorators import Debug


__author__ = "Omar Cusma Fait"
__date__ = (11, 3, 2020)
__version__ = "1.3.2"


if __name__ == '__main__':
    print('iter_utils', iter_utils.__version__)
    print('files', files.__version__)
    print(q_print, load_obj, save_obj, Debug)
