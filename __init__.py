"""         omar_utils

Provides common and useful methods of all kinds
Files are not supposed to depend on one another since they may be frequently updated
"""
from omar_utils.basic import iter_utils
from omar_utils.basic import files


__author__ = "Omar Cusma Fait"
__date__ = (26, 2, 2020)
__version__ = "1.3.0"


if __name__ == '__main__':
    print('iter_utils', iter_utils.__version__)
    print('files', files.__version__)
