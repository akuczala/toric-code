import itertools
from functools import reduce
from typing import List, Tuple

import numpy as np

from scipy import sparse


def tensor_product_flatten(mats):
    return reduce(
        lambda x, y: np.tensordot(x, y, axes=0).transpose(1, 2, 0, 3).reshape(x.shape[0] * y.shape[0], -1), mats)


def tensor_product_flatten_sparse(mats, verbose=False):
    def kron(a, b):
        if verbose:
            print(f"{a.shape}, {b.shape}")
        return sparse.kron(a, b, format='coo')

    return reduce(kron, (sparse.coo_array(mat) for mat in mats))


def comma_separated_string(iterable):
    return ''.join(
        f"{str(value)}, " for value in iterable
    )[:-2]


def make_site_grid_basis_vector(qubits: "List[Site[None]]", basis_index: int) -> np.ndarray:
    site_basis_index = int_to_bit_list(len(qubits), basis_index)
    grid_shape = qubits[0].GridPointClass.lengths
    grid = np.empty(grid_shape)
    for i, qubit in zip(site_basis_index, qubits):
        grid[qubit.pos[0], qubit.pos[1]] = 2 * i - 1
    return grid


def int_to_bit_list(n_bits: int, val: int) -> List[int]:
    return list(map(int, format(val, f'0{n_bits}b')))


def nearest_bounding_rectangle(n: int) -> Tuple[int, int]:
    rt = int(np.sqrt(n))
    factor = n // rt
    if rt * factor == n:
        return rt, factor
    else:
        assert (rt + 1) * factor >= rt * (factor + 1)
        return rt + 1, factor


class PrintDataclassMixin:

    def __str__(self):
        return f"{type(self).__name__}({comma_separated_string(self.__dict__.values())})"
