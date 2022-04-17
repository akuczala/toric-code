from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Dict

from scipy.sparse import coo_array

from qubit import Qubit
from toriccode.box import HasBox
from toriccode.grid_point import ContainsGridPoint
from toriccode.operators import Operator, OPERATOR_IDENTITY
from toriccode.utils import tensor_product_flatten_sparse


def operator_map_to_list(operator_map: Dict[int, Operator]) -> List[Operator]:
    return [operator_map[i] for i in range(len(operator_map))]


class Term:

    @property
    @abstractmethod
    def boxed_operators(self) -> List[HasBox[Operator]]:
        pass

    @staticmethod
    def get_qubits(terms: List["Term"]) -> List[HasBox[None]]:
        return list(set(
            boxed.with_new_content(None) for term in terms for boxed in term.boxed_operators
        ))

    def generate_matrix(self, qubits: Dict[HasBox[None], int], verbose=False) -> coo_array:
        operators = operator_map_to_list(
            self.identity_pad_operators(len(qubits), self.get_qubit_operators(qubits)))
        return tensor_product_flatten_sparse([op.matrix for op in operators], verbose=verbose)

    def get_qubit_operators(self, qubits: Dict[Qubit, int]) -> Dict[int, Operator]:
        # todo assert uniqueness on links in Term somewhere
        return {qubits[link.with_new_content(None)]: link.boxed_value for link in self.boxed_operators}

    @staticmethod
    def identity_pad_operators(n_qubits, qubits: Dict[int, Operator]) -> Dict[int, Operator]:
        return {
            i: qubits.get(
                i,
                OPERATOR_IDENTITY  # type: ignore
            ) for i in range(n_qubits)
        }


@dataclass(frozen=True)
class GenericTerm(Term):
    _boxed_operators: List[HasBox[Operator]]

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return self._boxed_operators


class LocalTerm(Term, ContainsGridPoint):
    pass
