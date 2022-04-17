from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum

import numpy as np


class Pauli(Enum):
    Z = 'Z'
    X = 'X'
    I = 'I'

    @property
    def matrix(self):
        return PAULI_MATRICES[self]

    def __str__(self):
        return self.value


PAULI_MATRICES = {
    Pauli.Z: np.array([[1, 0], [0, -1]]),
    Pauli.X: np.array([[0, 1], [1, 0]]),
    Pauli.I: np.eye(2)
}


class Operator(ABC):

    @property
    @abstractmethod
    def matrix(self) -> np.ndarray:
        pass


@dataclass(frozen=True)
class PauliOperator(Operator):
    pauli: Pauli

    @property
    def matrix(self) -> np.ndarray:
        return self.pauli.matrix

    # some metaprogramming here to autofill?
    @classmethod
    @property
    def Z(cls) -> "PauliOperator":
        return cls(Pauli.Z)

    @classmethod
    @property
    def X(cls) -> "PauliOperator":
        return cls(Pauli.X)

    @classmethod
    @property
    def I(cls) -> "PauliOperator":
        return cls(Pauli.I)

    def __str__(self):
        return str(self.pauli)


OPERATOR_IDENTITY = PauliOperator.I
