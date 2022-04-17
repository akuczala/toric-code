from typing import List

from scipy import sparse

from toriccode.hamiltonian import Hamiltonian
from toriccode.terms import Term
from toriccode.utils import list_inverse_map


class HamiltonianBuilder:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def build(self, local_terms: List[Term], coefs: List[float]) -> Hamiltonian:
        return Hamiltonian(self.build_matrix(local_terms, coefs), local_terms, coefs)

    def build_matrix(self, local_terms: List[Term], coefs: List[float]) -> sparse.coo_matrix:
        qubit_to_index_map = list_inverse_map(Term.get_qubits(local_terms))

        print("padding + tensor producting")
        return sum(
            coef * term.generate_matrix(qubit_to_index_map, verbose=self.verbose)
            for coef, term in zip(coefs, local_terms)
        )