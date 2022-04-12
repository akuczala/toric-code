from abc import abstractmethod
from dataclasses import dataclass
from typing import List

from toriccode.box import HasBox
from toriccode.grid_point import ContainsGridPoint
from toriccode.operators import Operator


class Term:

    @property
    @abstractmethod
    def boxed_operators(self) -> List[HasBox[Operator]]:
        pass


@dataclass(frozen=True)
class GenericTerm(Term):
    _boxed_operators: List[HasBox[Operator]]

    @property
    def boxed_operators(self) -> List[HasBox[Operator]]:
        return self._boxed_operators


class LocalTerm(Term, ContainsGridPoint):
    pass
