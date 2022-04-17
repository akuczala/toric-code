from typing import List, Dict

from scipy import sparse

from qubit import Qubit
from toriccode.hamiltonian import Hamiltonian
from toriccode.terms import Term
from toriccode.utils import list_inverse_map


class HamiltonianBuilder:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def build(self, local_terms: List[Term], coefs: List[float]) -> Hamiltonian:
        qubits = list_inverse_map(Term.get_qubits(local_terms))

        print("padding + tensor producting")
        matrix = self._build_matrix(qubits, local_terms, coefs)
        return Hamiltonian(qubits, local_terms, coefs, matrix)

    def _build_matrix(self, qubits: Dict[Qubit, int], local_terms: List[Term],
                      coefs: List[float]) -> sparse.coo_matrix:
        return sum(
            coef * term.generate_matrix(qubits, verbose=self.verbose)
            for coef, term in zip(coefs, local_terms)
        )
