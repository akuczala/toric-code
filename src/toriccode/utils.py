from functools import reduce

import numpy as np


def tensor_product(mats):
    return reduce(lambda x,y: np.tensordot(x,y, axes=0), mats)

def comma_separated_string(iterable):
    return ''.join(
        f"{str(value)}, " for value in iterable
    )[:-2]


class PrintDataclassMixin:

    def __str__(self):
        return f"{type(self).__name__}({comma_separated_string(self.__dict__.values())})"
