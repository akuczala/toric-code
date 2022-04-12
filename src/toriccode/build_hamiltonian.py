from dataclasses import dataclass
from typing import List, Dict, Iterable

from numpy import ndarray

from toriccode.operators import Operator, PauliOperator
from toriccode.terms import Term
from toriccode.utils import tensor_product_flatten


class HamiltonianBuilder:
    def __init__(self):
        pass

    @classmethod
    def build_matrix(cls, local_terms: List[Term]):
        qubits = Term.get_qubits(local_terms)
        # for i in range(254,256):
        #     plot_qubit_basis_vector(qubits, i)
        #     plt.show()

        qubit_to_index_map = {qubit: i for i, qubit in enumerate(qubits)}
        qubit_terms = [
            operator_map_to_list(cls.identity_pad_operators(len(qubits), cls.get_qubit_operators(term, qubit_to_index_map)))
            for term in local_terms
        ]
        return cls._build_matrix(qubit_terms)

    @staticmethod
    def _build_matrix(qubit_terms: List[List[Operator]]) -> ndarray:
        return sum(tensor_product_flatten([op.matrix for op in term]) for term in qubit_terms)  # type: ignore

    @staticmethod
    def get_qubit_operators(term: Term, qubit_to_index_map) -> Dict[int, Operator]:
        # todo assert uniqueness on links in Term somewhere
        return {qubit_to_index_map[link.with_new_content(None)]: link.boxed_value for link in term.boxed_operators}

    @staticmethod
    def identity_pad_operators(n_qubits, qubit_index_operator_map: Dict[int, Operator]) -> Dict[int, Operator]:
        return {
            i: qubit_index_operator_map.get(
                i,
                PauliOperator.I  # type: ignore
            ) for i in range(n_qubits)
        }


def operator_map_to_list(operator_map: Dict[int, Operator]) -> List[Operator]:
    return [operator_map[i] for i in range(len(operator_map))]