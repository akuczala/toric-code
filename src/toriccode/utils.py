from functools import reduce

import numpy as np


# np.tensordot requires some transposing before reshaping
def tensor_product(mats):
    return reduce(lambda x,y: np.tensordot(x,y, axes=0), mats)

def tensor_product_flatten(mats):
    return reduce(
        lambda x,y: np.tensordot(x,y, axes=0).transpose(1,2,0,3).reshape(x.shape[0] * y.shape[0], -1), mats)

def comma_separated_string(iterable):
    return ''.join(
        f"{str(value)}, " for value in iterable
    )[:-2]


class PrintDataclassMixin:

    def __str__(self):
        return f"{type(self).__name__}({comma_separated_string(self.__dict__.values())})"
