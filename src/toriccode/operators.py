from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum

import numpy as np


class Pauli(Enum):
    I = 'I'
    X = 'X'
    Y = 'Y'
    Z = 'Z'

    @property
    def matrix(self):
        return PAULI_MATRICES[self]

    def __str__(self):
        return self.value


PAULI_MATRICES = {
    Pauli.I: np.eye(2),
    Pauli.X: np.array([[0, 1], [1, 0]]),
    Pauli.Y: np.array([[0, -1j], [1j, 0]]),
    Pauli.Z: np.array([[1, 0], [0, -1]]),

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
    def Y(cls) -> "PauliOperator":
        return cls(Pauli.Y)

    @classmethod
    @property
    def I(cls) -> "PauliOperator":
        return cls(Pauli.I)

    def __str__(self):
        return str(self.pauli)


OPERATOR_IDENTITY = PauliOperator.I
