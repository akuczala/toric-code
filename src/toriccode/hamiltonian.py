from typing import List

import numpy as np
import scipy.linalg as lin
import scipy.sparse.linalg as slin
from scipy import sparse

from toriccode.terms import Term


class Hamiltonian:
    def __init__(self, matrix: sparse.coo_matrix, local_terms: List[Term], coefs: List[float]):
        self.matrix = matrix
        self.local_terms = local_terms
        self.coefs = coefs
        self.qubits = Term.get_qubits(local_terms)

    @property
    def dim(self) -> int:
        return self.matrix.shape[0]

    def calc_eigs(self, n_eigs=3, max_dense=1000):
        eigs, vecs = lin.eigh(self.matrix.toarray()) if self.dim < max_dense else slin.eigsh(self.matrix.tocsc(),
                                                                                             n_eigs)
        return (lambda argsort: (eigs[argsort], vecs[:, argsort]))(np.argsort(eigs))
