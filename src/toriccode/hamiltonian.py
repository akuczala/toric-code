from typing import List, Dict

import numpy as np
import scipy.linalg as lin
import scipy.sparse.linalg as slin
from scipy import sparse

from qubit import Qubit
from toriccode.terms import Term


class Hamiltonian:
    def __init__(self, qubits: Dict[Qubit, int], local_terms: List[Term], coefs: List[float], matrix: sparse.coo_matrix):
        self.matrix = matrix
        self.local_terms = local_terms
        self.coefs = coefs
        self.qubits = qubits

    @property
    def dim(self) -> int:
        return self.matrix.shape[0]

    def calc_eigs(self, n_eigs=3, max_dense=1000):
        eigs, vecs = lin.eigh(self.matrix.toarray()) if self.dim < max_dense else slin.eigsh(self.matrix.tocsc(),
                                                                                             n_eigs)
        return (lambda argsort: (eigs[argsort], vecs[:, argsort]))(np.argsort(eigs))
